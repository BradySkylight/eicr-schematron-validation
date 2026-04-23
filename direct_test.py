from pathlib import Path

from saxonche import PySaxonProcessor

BASE_FOLDER = Path(__file__).parent / "eicr-validator"

ECR_FOLDER = BASE_FOLDER / "eicr"
SCHEMA_FOLDER = BASE_FOLDER / "schematron"
XSLT_FOLDER = BASE_FOLDER / "schxslt"
OUTPUT_FOLDER = BASE_FOLDER / "output"

ecr_file = ECR_FOLDER / "Test2.xml"

APHL_SCHEMATRON = SCHEMA_FOLDER / "APHL_TextToCodeSchematron_09252025.sch"
APHL_SCHEMATRON_ERROR_FORMAT = SCHEMA_FOLDER / "Stitched_VS_report.xsl"
XSLT_INCLUDE = XSLT_FOLDER / "include.xsl"
XSLT_EXPAND = XSLT_FOLDER / "expand.xsl"
XSLT_COMPILE = XSLT_FOLDER / "compile-for-svrl.xsl"
STAGE1_OUTPUT = OUTPUT_FOLDER / "sch_error_result_WITH_ORG_FILE.xml"
STAGE2_OUTPUT = OUTPUT_FOLDER / "stage2.sch.tmp"
VALIDATOR_OUTPUT = OUTPUT_FOLDER / "validator.xsl.tmp"
VALIDATION_REPORT = OUTPUT_FOLDER / "validation_report.svrl"


try:
    with PySaxonProcessor(license=False) as proc:
        print(f"Saxon/C verion: {proc.version}")
        xsltproc = proc.new_xslt30_processor()
        print("--- Step 1: Process Includes If not already present ")

        xsltproc.transform_to_file(
            source_file=str(ecr_file),
            stylesheet_file=str(APHL_SCHEMATRON_ERROR_FORMAT),
            output_file=str(STAGE1_OUTPUT),
        )

except Exception as e:  # noqa: BLE001
    print(f"An error occurred during validation: {e}")
