from lib.matcher import Matcher

class EmailMatcher(Matcher):
    '''
    Reads csv file and groups records based on a given type.

    '''
    def __init__(self, source, match_type):
        super(EmailMatcher, self).__init__(source, match_type)

    def get_matching_record_values(self, record):
        '''
        Return the matching values from the current record.

        :param record: a typical row in the input file.
        :return: a list of values pertaining to the matching columns
        '''
        results = []
        for index in self.matching_columns:
            if record[index] != '':
                results.append(record[index])

        return tuple(results)


