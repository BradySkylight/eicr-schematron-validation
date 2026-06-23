#!/usr/bin/env python
import argparse
from encodings.punycode import T
from pathlib import Path

from saxonche import PySaxonProcessor

BASE_FOLDER = Path(__file__).parent / "eicr-validator"

ECR_FOLDER = BASE_FOLDER / "eicr"
SCHEMA_FOLDER = BASE_FOLDER / "schematron"
XSLT_FOLDER = BASE_FOLDER / "schxslt"
OUTPUT_FOLDER = BASE_FOLDER / "output"
RESULT_FOLDER = OUTPUT_FOLDER / "result"

APHL_SCHEMATRON = SCHEMA_FOLDER / "APHL_TextToCodeSchematron_09252025.sch"
APHL_SCHEMATRON_ERROR_FORMAT = SCHEMA_FOLDER / "aims_output" / "Stitched_VS_report_06052026.xsl"
XSLT_INCLUDE = XSLT_FOLDER / "include.xsl"
XSLT_EXPAND = XSLT_FOLDER / "expand.xsl"
XSLT_COMPILE = XSLT_FOLDER / "compile-for-svrl.xsl"
STAGE1_OUTPUT = OUTPUT_FOLDER / "stage1.sch.tmp"
STAGE2_OUTPUT = OUTPUT_FOLDER / "stage2.sch.tmp"
VALIDATOR_OUTPUT = OUTPUT_FOLDER / "validator.xsl.tmp"


def get_aims_output(file_name: str | None = None):
    try:
        with PySaxonProcessor(license=False) as proc:
            print(f"Saxon/C verion: {proc.version}")
            xsltproc = proc.new_xslt30_processor()
            print("--- Run schematron validation and produce AIMs output using 'Stiched' XSL!")

            for ecr_file_path in ECR_FOLDER.glob("*.xml"):
                if file_name is not None:
                    if ecr_file_path.name != file_name:
                        continue
                    print(f"For file {file_name}")
                else:
                    print(f" for ALL ECR files in {ECR_FOLDER}")

                print(f"and save results to {RESULT_FOLDER} ---")

                result_file = RESULT_FOLDER / f"{ecr_file_path.stem}_aims_schematron_errors.xml"

                xsltproc.transform_to_file(
                    source_file=str(ecr_file_path),
                    stylesheet_file=str(APHL_SCHEMATRON_ERROR_FORMAT),
                    output_file=str(result_file),
                )

    except Exception as e:  # noqa: BLE001
        print(f"An error occurred during validation: {e}")


def validate_eicr(file_name: str = None, redo_all_steps: bool = False):
    try:
        with PySaxonProcessor(license=False) as proc:
            print(f"Saxon/C verion: {proc.version}")
            xsltproc = proc.new_xslt30_processor()
            if redo_all_steps:
                print("Remove all previous files generated at all steps")
                STAGE1_OUTPUT.unlink(missing_ok=True)
                STAGE2_OUTPUT.unlink(missing_ok=True)
                VALIDATOR_OUTPUT.unlink(missing_ok=True)
            else:
                print("Will use existing files for Step 1-3")

            if not STAGE1_OUTPUT.exists():
                # Step 1: Process includes
                # Note: For schxslt, you typically apply the XSLT to the SCH file as the source
                print("--- Step 1: Process Includes against Schematron File")
                xsltproc.transform_to_file(
                    source_file=str(APHL_SCHEMATRON),
                    stylesheet_file=str(XSLT_INCLUDE),
                    output_file=str(STAGE1_OUTPUT),
                )

            if not STAGE2_OUTPUT.exists():
                # Step 2: Expand abstract rules
                print("--- Step 2: Expand abstract rules using output from Step 1")
                xsltproc.transform_to_file(
                    source_file=str(STAGE1_OUTPUT),
                    stylesheet_file=str(XSLT_EXPAND),
                    output_file=str(STAGE2_OUTPUT),
                )

            if not VALIDATOR_OUTPUT.exists():
                # Step 3: Compile to an SVRL-producing XSLT stylesheet
                print(
                    "--- Step 3: Compile to an SVRL-producing XSLT stylesheet ",
                    "using the output from Step 2",
                )
                xsltproc.transform_to_file(
                    source_file=str(STAGE2_OUTPUT),
                    stylesheet_file=str(XSLT_COMPILE),
                    output_file=str(VALIDATOR_OUTPUT),
                )

            for ecr_file_path in ECR_FOLDER.glob("*.xml"):
                print("--- Step 4: Validate XML using the generated XSLT from Step 3")
                if file_name is not None:
                    if ecr_file_path.name != file_name:
                        continue
                    print(f"For file {file_name}")
                else:
                    print(f" for ALL ECR files in {ECR_FOLDER}")

                print(f"and save results to {RESULT_FOLDER} ---")

                result_file = RESULT_FOLDER / f"{ecr_file_path.stem}_validation_report.svrl"
                # Step 4: Apply the generated XSLT to the source XML
                xsltproc.transform_to_file(
                    source_file=str(ecr_file_path),
                    stylesheet_file=str(VALIDATOR_OUTPUT),
                    output_file=str(result_file),
                )
                print(
                    f"--- Validation complete for {ecr_file_path.stem} ",
                    f"Report saved to {RESULT_FOLDER}",
                )
            print("--- Validation complete process complete for all ECR files. ---")

    except Exception as e:  # noqa: BLE001
        print(f"An error occurred during validation: {e}")


def main(
    validation: bool,  # noqa: FBT001
    aims_output: bool,  # noqa: FBT001
    file_name: str | None = None,
    redo_all_steps: bool = False,
):
    print("Starting eICR Validation")
    if file_name is not None:
        print(f"For eICR: {file_name}")
    if validation:
        print("Perform just standard eICR Validation using APHLs Schematron File!")
        validate_eicr(file_name, redo_all_steps)
    if aims_output:
        print("Perform validation and generate Expected AIMs output for eICR ")
        get_aims_output(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to perform various types of eICR Validation using APHL Standards!",
    )
    parser.add_argument(
        "--validation",
        action="store_true",
        help="Run Standard eICR Validation",
    )
    parser.add_argument(
        "--aims_output",
        action="store_true",
        help="Run eICR Validation to get expected AIMS Output",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="The name of the eICR file to validate - MUST BE IN THE 'eicr' folder",
    )
    parser.add_argument(
        "--redo_all_steps",
        action="store_true",
        help="If you want to re-perform all XSL steps in the validation process",
    )

    args = parser.parse_args()
    print(args)
    main(
        validation=args.validation,
        aims_output=args.aims_output,
        file_name=args.file,
        redo_all_steps=args.redo_all_steps,
    )
