import sys
sys.path.insert(0, "../../..")
import logging
from cmapPy.pandasGEXpress import setup_GCToo_logger as setup_logger
import unittest
import pandas as pd 
import pandas.util.testing as pandas_testing
from cmapPy.pandasGEXpress import parse 
from cmapPy.pandasGEXpress import mini_gctoo_for_testing as mini_gctoo_for_testing
from cmapPy.pandasGEXpress import slice_gct as slice_gct

from cmapPy.pandasGEXpress import GCToo as GCToo 
from cmapPy.pandasGEXpress import parse_gctx as parse_gctx
from cmapPy.pandasGEXpress import mini_gctoo_for_testing as mini_gctoo_for_testing

__author__ = "Oana Enache"
__email__ = "oana@broadinstitute.org"

FUNCTIONAL_TESTS_PATH = "functional_tests"

logger = logging.getLogger(setup_logger.LOGGER_NAME)

class TestParse(unittest.TestCase):
    def test_gctx_parsing(self):
        # parse in gctx, no other arguments        
        mg1 = mini_gctoo_for_testing.make()
        mg2 = parse("functional_tests/mini_gctoo_for_testing.gctx")

        pandas_testing.assert_frame_equal(mg1.data_df, mg2.data_df)
        pandas_testing.assert_frame_equal(mg1.row_metadata_df, mg2.row_metadata_df)
        pandas_testing.assert_frame_equal(mg1.col_metadata_df, mg2.col_metadata_df) 

        # check convert_neg_666 worked correctly
        self.assertTrue(mg2.col_metadata_df["mfc_plate_id"].isnull().all())

        # parse w/o convert_neg_666
        mg2_alt = parse("functional_tests/mini_gctoo_for_testing.gctx", convert_neg_666 = False)
        self.assertFalse(mg2_alt.col_metadata_df["mfc_plate_id"].isnull().all())        

        # parsing w/rids & cids specified 
        test_rids = ['LJP007_MCF10A_24H:TRT_CP:BRD-K93918653:3.33', 'LJP007_MCF7_24H:CTL_VEHICLE:DMSO:-666']
        test_cids = ['LJP007_MCF7_24H:TRT_POSCON:BRD-A61304759:10']
        mg3 = slice_gct.slice_gctoo(mg1, rid=test_rids, cid=test_cids)
        mg4 = parse("functional_tests/mini_gctoo_for_testing.gctx",
                               rid=test_rids, cid=test_cids)
        pandas_testing.assert_frame_equal(mg3.data_df, mg4.data_df)
        pandas_testing.assert_frame_equal(mg3.row_metadata_df, mg4.row_metadata_df)
        pandas_testing.assert_frame_equal(mg3.col_metadata_df, mg4.col_metadata_df)

        # parsing w/ridx & cidx specified 
        mg5 = slice_gct.slice_gctoo(mg1, rid=['LJP007_MCF7_24H:CTL_VEHICLE:DMSO:-666'],
                                    cid='LJP007_MCF7_24H:CTL_VEHICLE:DMSO:-666')
        mg6 = parse("functional_tests/mini_gctoo_for_testing.gctx", ridx=[4], cidx=[4])

        pandas_testing.assert_frame_equal(mg5.data_df, mg6.data_df)
        pandas_testing.assert_frame_equal(mg5.row_metadata_df, mg6.row_metadata_df)
        pandas_testing.assert_frame_equal(mg5.col_metadata_df, mg6.col_metadata_df)

        # parsing row metadata only
        mg7 = parse("functional_tests/mini_gctoo_for_testing.gctx", row_meta_only=True)
        pandas_testing.assert_frame_equal(mg7, mg1.row_metadata_df)

        # parsing col metadata only
        mg8 = parse("functional_tests/mini_gctoo_for_testing.gctx", col_meta_only=True)
        pandas_testing.assert_frame_equal(mg8, mg1.col_metadata_df)

        # parsing w/multiindex
        mg9 = parse("functional_tests/mini_gctoo_for_testing.gctx", make_multiindex=True)
        self.assertTrue(mg9.multi_index_df is not None)

    def test_gct_parsing(self):
        # parse in gct, no other arguments
        mg1 = mini_gctoo_for_testing.make()
        mg2 = parse("functional_tests/mini_gctoo_for_testing.gct")

        pandas_testing.assert_frame_equal(mg1.data_df, mg2.data_df)
        pandas_testing.assert_frame_equal(mg1.row_metadata_df, mg2.row_metadata_df)
        pandas_testing.assert_frame_equal(mg1.col_metadata_df, mg2.col_metadata_df) 

        # check convert_neg_666 worked correctly
        self.assertTrue(mg2.col_metadata_df["mfc_plate_id"].isnull().all())

        # parse w/o convert_neg_666
        mg2_alt = parse("functional_tests/mini_gctoo_for_testing.gct", convert_neg_666 = False)
        self.assertFalse(mg2_alt.col_metadata_df["mfc_plate_id"].isnull().all())        

        # check unused rid argument handling
        with self.assertRaises(Exception) as context:
            mg3 = parse("functional_tests/mini_gctoo_for_testing.gct", rid=["a"])
        self.assertTrue("parse_gct does not use the argument" in str(context.exception))

        # check unused cid argument handling 
        with self.assertRaises(Exception) as context:
            mg4 = parse("functional_tests/mini_gctoo_for_testing.gct", cid=["a"])
        self.assertTrue("parse_gct does not use the argument" in str(context.exception))        

        # check unused ridx argument handling
        with self.assertRaises(Exception) as context:
            mg5 = parse("functional_tests/mini_gctoo_for_testing.gct", ridx=[0])
        self.assertTrue("parse_gct does not use the argument" in str(context.exception))

        # check unused cidx argument handling 
        with self.assertRaises(Exception) as context:
            mg6 = parse("functional_tests/mini_gctoo_for_testing.gct", cidx=[0])
        self.assertTrue("parse_gct does not use the argument" in str(context.exception))

if __name__ == "__main__":
    setup_logger.setup(verbose=True)
    unittest.main()



