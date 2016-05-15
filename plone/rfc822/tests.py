from plone.testing import layered
from plone.testing.zca import UNIT_TESTING
import doctest
import re
import sys
import unittest


DOCFILES = [
    'message.txt',
    'fields.txt',
    'supermodel.txt',
]

SKIP_PYTHON_2 = doctest.register_optionflag('SKIP_PYTHON_2')
SKIP_PYTHON_3 = doctest.register_optionflag('SKIP_PYTHON_3')
IGNORE_U = doctest.register_optionflag('IGNORE_U')
IGNORE_B = doctest.register_optionflag('IGNORE_B')


class PolyglotOutputChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        if optionflags & SKIP_PYTHON_3 and sys.version_info >= (3,):
            return True
        elif optionflags & SKIP_PYTHON_2:
            return True

        if hasattr(self, '_toAscii'):
            got = self._toAscii(got)
            want = self._toAscii(want)

        # Naive fix for comparing unicode strings
        if got != want and optionflags & IGNORE_U:
            got = re.sub(r'^u([\'"])', r'\1', got)
            want = re.sub(r'^u([\'"])', r'\1', want)

        # Naive fix for comparing byte strings
        if got != want and optionflags & IGNORE_B:
            got = re.sub(r'^b([\'"])', r'\1', got)
            want = re.sub(r'^b([\'"])', r'\1', want)

        return doctest.OutputChecker.check_output(
            self, want, got, optionflags)


def test_suite():

    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                docfile,
                checker=PolyglotOutputChecker(),
                optionflags=doctest.ELLIPSIS,
            ),
            layer=UNIT_TESTING
        )
        for docfile in DOCFILES
    ])
    return suite
