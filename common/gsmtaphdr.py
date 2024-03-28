import ctypes

class GsmtapHdr(ctypes.BigEndianStructure):
    _pack_ = 1
    # Based on gsmtap_hdr structure in <grgsm/gsmtap.h> from gr-gsm
    _fields_ = [
        ("version", ctypes.c_uint8),
        ("hdr_len", ctypes.c_uint8),
        ("type", ctypes.c_uint8),
        ("timeslot", ctypes.c_uint8),
        ("arfcn", ctypes.c_uint16),
        ("signal_dbm", ctypes.c_int8),
        ("snr_db", ctypes.c_int8),
        ("frame_number", ctypes.c_uint32),
        ("sub_type", ctypes.c_uint8),
        ("antenna_nr", ctypes.c_uint8),
        ("sub_slot", ctypes.c_uint8),
        ("res", ctypes.c_uint8),
    ]

    def __repr__(self):
        return "%s(version=%d, hdr_len=%d, type=%d, timeslot=%d, arfcn=%d, signal_dbm=%d, snr_db=%d, frame_number=%d, sub_type=%d, antenna_nr=%d, sub_slot=%d, res=%d)" % (
            self.__class__, self.version, self.hdr_len, self.type,
            self.timeslot, self.arfcn, self.signal_dbm, self.snr_db,
            self.frame_number, self.sub_type, self.antenna_nr, self.sub_slot,
            self.res,
        )
