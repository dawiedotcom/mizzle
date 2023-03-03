
class Protocol:

    units = {
        
    }

    def parse(self, txt):
        return None

class NMEA(Protocol):
    def parse(self, timestamp, txt):
        if '*' in txt:
            q, checksum = txt.split('*')
        else:
            q = txt
            checksum = ''
        tokens = q.split(',')
        if tokens[0] == '$WIXDR':
            return self._parse_xdr(timestamp, tokens[1:], checksum)
        if tokens[0] == '$WIMWV':
            return self._parse_mwv(timestamp, tokens[1:], checksum)
        else:
            raise Exception(f"Unknown NMEA command: {tokens[0]}")

    def _parse_xdr(self, timestamp, tokens, checksum):
        # Parse measument responses from XDR queries.
        if len(tokens) % 4 > 0:
            raise Exception("NMEA XDR tokens should be a multiple of 4.")

        measurements = []
        while len(tokens) > 0:
            transducer_type = tokens.pop(0)
            measurement_data = tokens.pop(0)
            measurement_units = tokens.pop(0)
            transducer_id = tokens.pop(0)

            measurement_data = float(measurement_data)

            measurements.append((
                timestamp,
                measurement_data,
                transducer_type + transducer_id,
                transducer_type + measurement_units,
            ))

        return measurements

    def _parse_mwv(self, timestamp, tokens, checksum):
        # Parse measument responses from MVW (wind direction) queries.
        if len(tokens) != 5:
            raise Exception("NMEA MWV must have 5 tokens.")

        if tokens[4] == 'V':
            return None

        return (
            timestamp,
            float(tokens[0]),
            float(tokens[2]),
        )

