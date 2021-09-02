class Airport:
    """ Airport as represented in <filename>.csv or <filename>.xls"""

    prop_names = ('id', 'name', 'city', 'country', 'iata', 'icao','lat', 'long', 'alt', 'utc_offset', 'dst_rule', 'tz', 'type', 'source')

    def __init__(self, csv_entry):
        assert len(csv_entry) == len(Airport.prop_names)
        self.__dict__.update(dict(zip(Airport.prop_names, csv_entry)))

    def __str__(self):
        return "{0.iata} ({0.name})".format(self)