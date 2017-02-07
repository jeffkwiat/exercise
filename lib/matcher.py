import abc
import os

class Matcher(object):
    '''
    Reads csv file and groups records based on a given type.

    '''

    def __init__(self, source, match_type):
        self.source = os.path.normpath(source)
        self.match_type = match_type
        self.records = self.get_records()
        self.columns = []
        self.matching_columns = []

    @abc.abstractmethod
    def get_matching_columns(self, header_row):
        '''
        Return a list of column indices that should be used
        to match.
        '''
        pass

    @abc.abstractmethod
    def get_matching_record_values(self, record):
        '''
        Return a list of column indices that should be used
        to match.

        '''
        pass

    def get_matching_columns(self, columns):
        '''

        :param header_row:
        :return: the list of column indices we should use to match.
        '''
        column_indices = []
        for column_index in range(len(columns)):
            if columns[column_index].lower().startswith(self.match_type):
                column_indices.append(column_index)
        return column_indices

    def get_matching_record_values(self, record):
        '''
        Return the matching values from the current record.

        :param record: a typical row in the input file.
        :return: a list of values pertaining to the matching columns
        '''

        return tuple([record[index] for index in self.matching_columns])

    def get_output(self):
        '''
        Create an output file based on the given input file.

        '''
        return self.source.replace('.csv', '.output.csv')

    def get_records(self):
        '''
        Read data from source file and return a list of records.

        NOTE:  Assumes the first row is the header.

        '''
        records = []

        # The default input files are showing as one line separated by \r,
        # so I opted for this approach instead of using the csv library.
        # In a production sense, I would consult with whomever provided
        # the files.
        header_row = True
        for line in open(self.source).read().split('\n'):
            record = line.strip().split(',')
            if self.is_valid_record(record):
                if header_row:
                    self.columns = record
                    self.matching_columns = self.get_matching_columns(record)
                    header_row = False
                    continue

                records.append(record)

        return records

    def is_valid_record(self, record):
        '''

        :param record: a record from the file as a list.
        :return: True if this record is valid.  Otherwise, False.
        '''

        # Due to the input file issue, I opted for this apprach.
        return len(record) > 1

    def write_output(self, records):
        '''
        Write records to external file.

        :param records: a list of records to write to a file.
        :return: Nothing.
        '''
        with open(self.get_output(), mode='wt') as output:
            output.write('%s\n' % ','.join(self.columns))
            for record in records:
                output.write('%s\n' % ','.join(record))

    def match(self):
        ids = {}
        current_id = 1
        records = self.get_records()
        results = []

        for record in records:
            same_record = False
            for key in self.get_matching_record_values(record):
                if key not in ids:
                    ids[key] = current_id
                    if not same_record:
                        current_id += 1
                        same_record = True

        for record in records:
            found = False
            for key in self.get_matching_record_values(record):
                if key in ids:
                    record.insert(0, str(ids[key]))
                    found = True
                    break

            if not found:
                record.insert(0, '0')

            results.append(record)


        self.write_output(results)