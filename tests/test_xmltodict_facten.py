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

