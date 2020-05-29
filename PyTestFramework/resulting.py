

class Result:
    def __init__(self):
        self.result_file = open('results/result.log', 'w')

    def start_test(self, file_name):
        #print('Testing of {} was started.'.format(file_name))
        self.result_file.write('\n\nTesting of {} was started\n'.format(file_name))

    def start_case(self, test_name):
        #print("Test case '{}'.".format(test_name))
        self.result_file.write("\n\nTest case '{}'".format(test_name))

    def add_pass(self, query, actual_result):
        #print("PASS. Result is '{0}' as expected. Query: {1}".format(actual_result, query))
        self.result_file.write("\nPASS. Result is '{0}' as expected"
                               "\n\tQuery: {1}".format(actual_result, query))

    def add_fail(self, query, actual_result, expected_result):
        #print("FAIL. Result is '{0}', but expected '{1}'. Query: {2}".format(actual_result, expected_result, query))
        self.result_file.write("\nFAIL. Result is '{0}', but expected '{1}'"
                               "\n\tQuery: {2}".format(actual_result, expected_result, query))

    def finish_test(self):
        self.result_file.close()