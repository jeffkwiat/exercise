import optparse

from lib.matchers.email_matcher import EmailMatcher
from lib.matchers.phone_matcher import PhoneMatcher
from lib.matchers.email_or_phone_matcher import EmailOrPhoneMatcher

if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('-s', '--source',
                      action='store', dest='source',
                      help='The path to the input file you are attempting to parse.')
    parser.add_option('-m', '--match_type',
                      action='store', dest='match_type',
                      help='How you wish to match the objects.')

    options, args = parser.parse_args()
    print('args: %s and %s' % (options.source, options.match_type))

    if options.match_type == 'email':
        matcher = EmailMatcher(options.source, options.match_type)
        matcher.match()
    elif options.match_type == 'phone':
        matcher = PhoneMatcher(options.source, options.match_type)
        matcher.match()
    elif options.match_type == 'phone_or_email':
        matcher = EmailOrPhoneMatcher(options.source, options.match_type)
        matcher.match()

    print('Done...')