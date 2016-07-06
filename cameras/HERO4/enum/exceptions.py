class KeyNotFoundException(Exception):
    def __init__(self, search_key, message='No information could be found for key {key}'):
        # Call the base class constructor with the parameters it needs
        message = message.format(key=search_key)
        super(KeyNotFoundException, self).__init__(message)

        # Custom values
        self.search_key = search_key


class ValueForExistingKeyNotFoundException(Exception):
    # the name is terrible, BUT it is descriptive
    def __init__(self, search_key, search_value, found_key,
                 message='No value information could be found for key {key} and value {value}'):
        message = message.format(key=search_key, value=search_value)
        # Call the base class constructor with the parameters it needs
        super(ValueForExistingKeyNotFoundException, self).__init__(message)

        # Custom values
        self.search_key = search_key
        self.search_value = search_value
        self.found_key = found_key
