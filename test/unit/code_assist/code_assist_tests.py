import os
import unittest
from test.lib.test_helper import MavensMateTest
base_test_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class CodeAssistTest(MavensMateTest):
    
    def test_should_return_list_of_methods(self): 
        data = """
        public with sharing class AUTOTEST {

            String someString;
            public String myPublicString { get; set; }

            public AUTOTEST(String foo , Boolean bar) {
                ApexPages.StandardController c;
                c.cancel();
                String s = 'foo';
                s.
        """
        stdin = {
            "data" : data.strip(),
            "file_name" : os.path.join(base_test_directory, 'unit', 'code_assist', 'test', 'classes', 'AUTOTEST.cls')
        }
        mm_response = self.runCommand(['mm.py', '-o', 'get_apex_class_completions', '--offline'], stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'string')

    def test_should_assist_inner_class(self): 
        data = """
        public with sharing class AUTOTEST {

            public MyClass {
                public String foo;
                public Boolean bar;
            }

            public AUTOTEST(String foo , Boolean bar) {
                MyClass c = new MyClass();
                c.
        """
        stdin = {
            "data" : data.strip(),
            "file_name" : os.path.join(base_test_directory, 'unit', 'code_assist', 'test', 'classes', 'AUTOTEST.cls')
        }
        mm_response = self.runCommand(['mm.py', '-o', 'get_apex_class_completions', '--offline'], stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'string')

    def test_should_return_list_of_apex_classes_and_objects(self): 
        mm_response = self.runCommand(['mm.py', '-o', 'get_apex_classes_and_objects', '--offline'], {})
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'string')

    def test_should_return_visualforce_tags(self): 
        mm_response = self.runCommand(['mm.py', '-o', 'get_visualforce_tags_list', '--offline'], {})
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'array')
        self.assertTrue('apex:actionFunction' in mm_response['body'])

    def test_should_return_visualforce_attributes_for_action_function_tag(self): 
        mm_response = self.runCommand(['mm.py', '-o', 'get_visualforce_attribute_list', '--offline'], {'tag':'apex:actionFunction'})
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'array')
        self.assertTrue(len(mm_response['body']) > 0)

    def test_should_return_string_type(self): 
        data = """
        public with sharing class AUTOTEST {

            String someString;
            public String myPublicString { get; set; }

            public AUTOTEST(String foo , Boolean bar) {
                ApexPages.StandardController c;
                c.cancel();
                String s = 'foo';
                s.
        """
        stdin = {
            "data" : data.strip()
        }
        
        mm_response = self.runCommand(['mm.py', '-o', 'get_apex_type_definition', '--offline'], stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'array')
        self.assertEqual(mm_response['body'][0], 9) # instantiation line number
        self.assertEqual(mm_response['body'][2], 'String') # type
        self.assertEqual(mm_response['body'][3], 's') # variable name

    def test_should_return_boolean_type(self): 
        data = """
        public with sharing class AUTOTEST {

            String someString;
            public Boolean myPublicString = true

            public AUTOTEST(String foo , Boolean bar) {
                myPublicString.
        """
        stdin = {
            "data" : data.strip()
        }
        
        mm_response = self.runCommand(['mm.py', '-o', 'get_apex_type_definition', '--offline'], stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'array')
        self.assertEqual(mm_response['body'][0], 4) # instantiation line number
        self.assertEqual(mm_response['body'][2], 'Boolean')
        self.assertEqual(mm_response['body'][3], 'myPublicString')

    def test_should_return_static_string_type(self): 
        data = """
        public with sharing class AUTOTEST {

            public static String someString;
            public Boolean myPublicString = true

            public AUTOTEST(String foo , Boolean bar) {
                someString.
        """
        stdin = {
            "data" : data.strip()
        }
        
        mm_response = self.runCommand(['mm.py', '-o', 'get_apex_type_definition', '--offline'], stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(mm_response['body_type'], 'array')
        self.assertEqual(mm_response['body'][0], 3) # instantiation line number
        self.assertEqual(mm_response['body'][2], 'String')
        self.assertEqual(mm_response['body'][3], 'someString')

if __name__ == '__main__':
    unittest.main()