from xmltodict import parse, ParsingInterrupted
import collections
import unittest

class XMLToDictFactenTestCase(unittest.TestCase):

    def test_force_flatten_callable(self):
        xml = """
        <config>
            <flatten>
                <server>
                    <name>server1</name>
                    <os>os1</os>
                </server>
            </flatten>
            <noflatten>
              <server>
                <name>server1</name>
                <os>os1</os>
              </server>
            </noflatten>
        </config>
        """

        def flatten(path, key):
            return key == 'flatten'

        expectedResult = {
            'config': {
                'flatten': 'server1os1',
                'noflatten': {
                    'server': {
                        'name': 'server1',
                        'os': 'os1',
                    },
                },
            }
        }

        self.assertEqual(expectedResult,
                         parse(xml,
                               flatten=flatten,
                               dict_constructor=dict))

    def test_force_flatten_callable_with_lists(self):
        xml = """
        <config>
            <flatten_force_list>
                <server>
                    <name>server1</name>
                    <os>os1</os>
                </server>
            </flatten_force_list>
            <flatten_list>
              <server>
                <name>server1</name>
                <os>os1</os>
              </server>
              <server>
                <name>server2</name>
                <os>os2</os>
              </server>
            </flatten_list>
        </config>
        """

        def flatten(path, key):
            return key == 'server'

        def force_list(path, key, value):
            #
            # must check that path is defined!
            # otherwise, path[-1] raises exception and
            # that this interfers weirdly with the logic of force_list
            #
            return path and (path[-1][0] == 'flatten_force_list') and (key == 'server')


        expectedResult = {
            'config': {
                'flatten_force_list': {'server': ['server1os1']},
                'flatten_list': {'server': ['server1os1', 'server2os2']},
            }
        }

        self.assertEqual(expectedResult,
                         parse(xml,
                               flatten=flatten,
                               force_list=force_list,
                               dict_constructor=dict))

    def test_force_flatten_callable_with_attribs(self):
        xml = """
        <config>
            <flatten>
                <server myattrib="hi">
                    <name myotherattrib="hello">server1</name>
                    <os>os1</os>
                </server>
            </flatten>
            <noflatten>
              <server>
                <name>server1</name>
                <os>os1</os>
              </server>
            </noflatten>
        </config>
        """

        def flatten(path, key):
            return key == 'flatten'

        expectedResult = {
            'config': {
                'flatten': 'server1os1',
                'noflatten': {
                    'server': {
                        'name': 'server1',
                        'os': 'os1',
                    },
                },
            }
        }

        self.assertEqual(expectedResult,
                         parse(xml,
                               flatten=flatten,
                               dict_constructor=dict))

    def test_force_flatten_callable_noop(self):
        xml = """
        <config>
            <noflatten>
              <server>
                <name>server1</name>
                <os>os1</os>
              </server>
            </noflatten>
        </config>
        """

        def flatten(path, key):
            return key == 'os'

        expectedResult = {
            'config': {
                'noflatten': {
                    'server': {
                        'name': 'server1',
                        'os': 'os1',
                    },
                },
            }
        }

        self.assertEqual(expectedResult,
                         parse(xml,
                               flatten=flatten,
                               dict_constructor=dict))

