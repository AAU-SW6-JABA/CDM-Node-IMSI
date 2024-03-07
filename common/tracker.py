import datetime
import time

from route_guide_pb2_grpc import RoutesStub
from route_guide_pb2 import LogMeasurementRequest
from .grpc_server import GrpcRequests


class Tracker:
    imsistate = {}
    # Phones
    imsis = []  # [IMSI,...]
    tmsis = {}  # {TMSI:IMSI,...}
    nb_IMSI = 0  # count the number of IMSI

    mcc = ""
    mnc = ""
    lac = ""
    cell = ""
    country = ""
    brand = ""
    operator = ""

    # in minutes
    purgeTimer = 10  # default 10 min

    mcc_codes = None
    sqlite_con = None
    mysql_con = None
    mysql_cur = None
    textfilePath = None
    output_function = None

    stub: RoutesStub
    antenna_id: int

    def __init__(self, stub: RoutesStub, antenna_id: int):
        self.output_function = self.output
        self.stub = stub
        self.antenna_id = antenna_id

    def set_output_function(self, new_output_function):
        # New output function need this field :
        # cpt, tmsi1, tmsi2, imsi, imsicountry, imsibrand, imsioperator, mcc, mnc, lac, cell, timestamp, packet=None
        self.output_function = new_output_function

    # return something like '0xd9605460'
    def str_tmsi(self, tmsi):
        if tmsi != "":
            new_tmsi = "0x"
            for a in tmsi:
                c = hex(a)
                if len(c) == 4:
                    new_tmsi += str(c[2]) + str(c[3])
                else:
                    new_tmsi += "0" + str(c[2])
            return new_tmsi
        else:
            return ""

    def current_cell(self, mcc, mnc, lac, cell):
        brand = ""
        operator = ""
        country = ""
        if mcc in self.mcc_codes and mnc in self.mcc_codes[mcc]:
            brand, operator, country, _ = self.mcc_codes[mcc][mnc]
        else:
            country = f"Unknown MCC {mcc}"
            brand = f"Unknown MNC {mnc}"
            operator = f"Unknown MNC {mnc}"
        self.mcc = str(mcc)
        self.mnc = str(mnc)
        self.lac = str(lac)
        self.cell = str(cell)
        self.country = country
        self.brand = brand
        self.operator = operator

    def output(self, cpt, tmsi1, tmsi2, imsi, mcc, mnc, lac, cell, now, signal):
        print(
            f"{str(cpt):7s} ; {str(tmsi1):10s} ; {str(tmsi2):10s} ; {str(imsi):17s} ; {str(mcc):4s} ; {str(mnc):5s} ; {str(lac):6s} ; {str(cell):6s} ; {now.isoformat():s} ; {now.isoformat():s} ; {str(signal):s}")

    def pfields(self, cpt, tmsi1, tmsi2, imsi, mcc, mnc, lac, cell, signal):
        if imsi:
            imsi = imsi
        else:
            imsi = ""
        now = datetime.datetime.now()
        self.output_function(cpt, tmsi1, tmsi2, imsi, mcc, mnc, lac, cell, now, signal)

    def header(self):
        print(
            f"{'Nb IMSI':7s} ; {'TMSI-1':10s} ; {'TMSI-2':10s} ; {'IMSI':17s} ; {'MCC':4s} ; {'MNC':5s} ; {'LAC':6s} ; {'CellId':6s} ; {'Timestamp':s} ; {'Signal_db':s}")

    # TODO: Add relevant code (Only the signal has been added)
    def register_imsi(self, arfcn, signal_dbm, imsi1="", imsi2="", tmsi1="", tmsi2=""):
        do_print = False
        tmsi1 = self.str_tmsi(tmsi1)
        tmsi2 = self.str_tmsi(tmsi2)

        if imsi1 and self.register_identifier(arfcn, imsi1, tmsi1, tmsi2, signal_dbm):
            do_print = True

        if imsi2 and self.register_identifier(arfcn, imsi2, tmsi1, tmsi2, signal_dbm):
            do_print = True

        # Unreachable or rarely reached branch? Add unit-test.
        if not imsi1 and not imsi2 and tmsi1 and tmsi2:
            if self.tmsis and tmsi2 in self.tmsis:
                # switch the TMSI
                do_print = True
                imsi1 = self.tmsis[tmsi2]
                self.tmsis[tmsi1] = imsi1
                del self.tmsis[tmsi2]

        if do_print:
            if imsi1:
                self.pfields(str(self.nb_IMSI),
                             tmsi1,
                             tmsi2,
                             imsi1,
                             self.mcc,
                             self.mnc,
                             self.lac,
                             self.cell,
                             signal_dbm)
            if imsi2:
                self.pfields(str(self.nb_IMSI),
                             tmsi1,
                             tmsi2,
                             imsi2,
                             self.mcc,
                             self.mnc,
                             self.lac,
                             self.cell,
                             signal_dbm)

        if not imsi1 and not imsi2:
            # Register IMSI as seen if a TMSI believed to belong to the IMSI is seen.
            if self.tmsis and tmsi1 and tmsi1 in self.tmsis and "" != self.tmsis[tmsi1]:
                self.imsi_seen(self.tmsis[tmsi1], arfcn, signal_dbm)

    def register_identifier(self, arfcn, imsi: str, tmsi1: str, tmsi2: str, signal_dbm) -> bool:
        registered_new: bool = False

        if imsi:
            self.imsi_seen(imsi, arfcn, signal_dbm)
            if imsi not in self.imsis:
                # new IMSI
                self.imsis.append(imsi)
                self.nb_IMSI += 1
                registered_new = True
            if self.tmsis and tmsi1 and (tmsi1 not in self.tmsis or self.tmsis[tmsi1] != imsi):
                # new TMSI to an ISMI
                self.tmsis[tmsi1] = imsi
                registered_new = True
            if self.tmsis and tmsi2 and (tmsi2 not in self.tmsis or self.tmsis[tmsi2] != imsi):
                # new TMSI to an ISMI
                self.tmsis[tmsi2] = imsi
                registered_new = True

        return registered_new

    def imsi_seen(self, imsi, arfcn, signal_dbm):
        now = datetime.datetime.utcnow().replace(microsecond=0)
        if imsi in self.imsistate:
            self.imsistate[imsi]["lastseen"] = now
        else:
            self.imsistate[imsi] = {
                "firstseen": now,
                "lastseen": now,
                "imsi": imsi,
                "arfcn": arfcn,
            }
        self.imsi_purge_old()

        # Create grpc message and
        grpc_message = LogMeasurementRequest(
            aid=self.antenna_id,
            imsi=imsi,
            timestamp=time.time(),
            signal_strength=signal_dbm)

        GrpcRequests.log_measurement(self.stub, grpc_message)

    def imsi_purge_old(self):
        now = datetime.datetime.utcnow().replace(microsecond=0)
        maxage = datetime.timedelta(minutes=self.purgeTimer)
        limit = now - maxage
        remove = [imsi for imsi in self.imsistate if limit > self.imsistate[imsi]["lastseen"]]
        for k in remove:
            del self.imsistate[k]