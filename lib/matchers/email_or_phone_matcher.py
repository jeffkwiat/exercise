import re

from lib.matcher import Matcher

class EmailOrPhoneMatcher(Matcher):
    '''
    Reads csv file and groups records based on a given type.

    '''

    def __init__(self, source, match_type):
        super(EmailOrPhoneMatcher, self).__init__(source, match_type)

    def get_matching_columns(self, columns):
        '''

        :param header_row:
        :return: the list of column indices we should use to match.
        '''
        column_indices = []
        for column_index in range(len(columns)):
            if columns[column_index].lower().startswith('phone') or \
                columns[column_index].lower().startswith('email'):
                column_indices.append(column_index)
        return column_indices

    def get_matching_record_values(self, record):
        '''
        Return the matching values from the current record.

        :param record: a typical row in the input file.
        :return: a list of values pertaining to the matching columns
        '''
        values = []

        for index in self.matching_columns:
            cell = record[index]

            if cell.strip() != '':

                # if this is an email address, add it.
                if '@' in cell:
                    values.append(cell)

                # else, if this is a phone, format it.
                else:
                    out = re.sub('[\s\(\)\.\-]', '', record[index])
                    if len(out) == 10:
                        out = '1%s' % out
                    values.append(out)

        return tuple(values)