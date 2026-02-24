from pathlib import Path

from saxonche import PySaxonProcessor

BASE_FOLDER = Path(__file__).parent / "eicr-validator"

ECR_FOLDER = BASE_FOLDER / "eicr"
SCHEMA_FOLDER = BASE_FOLDER / "schematron"
XSLT_FOLDER = BASE_FOLDER / "schxslt"
OUTPUT_FOLDER = BASE_FOLDER / "output"

APHL_SCHEMATRON = SCHEMA_FOLDER / "APHL_TextToCodeSchematron_09252025.sch"
XSLT_INCLUDE = XSLT_FOLDER / "include.xsl"
XSLT_EXPAND = XSLT_FOLDER / "expand.xsl"
XSLT_COMPILE = XSLT_FOLDER / "compile-for-svrl.xsl"
STAGE1_OUTPUT = OUTPUT_FOLDER / "stage1.sch.tmp"
STAGE2_OUTPUT = OUTPUT_FOLDER / "stage2.sch.tmp"
VALIDATOR_OUTPUT = OUTPUT_FOLDER / "validator.xsl.tmp"
VALIDATION_REPORT = OUTPUT_FOLDER / "validation_report.svrl"


try:
    with PySaxonProcessor(license=False) as proc:
        print(f"Saxon/C verion: {proc.version}")
        xsltproc = proc.new_xslt30_processor()
        print("--- Step 1: Process Includes If not already present ")

        if not STAGE1_OUTPUT.exists():
            # Step 1: Process includes
            # Note: For schxslt, you typically apply the XSLT to the SCH file as the source
            xsltproc.transform_to_file(
                source_file=str(APHL_SCHEMATRON),
                stylesheet_file=str(XSLT_INCLUDE),
                output_file=str(STAGE1_OUTPUT),
            )

        print("--- Step 2: Expand abstract rules If not already present ")
        if not STAGE2_OUTPUT.exists():
            # Step 2: Expand abstract rules
            xsltproc.transform_to_file(
                source_file=str(STAGE1_OUTPUT),
                stylesheet_file=str(XSLT_EXPAND),
                output_file=str(STAGE2_OUTPUT),
            )

        print("--- Step 3: Compile to an SVRL-producing XSLT stylesheet If not already present ")
        if not VALIDATOR_OUTPUT.exists():
            # Step 3: Compile to an SVRL-producing XSLT stylesheet
            xsltproc.transform_to_file(
                source_file=str(STAGE2_OUTPUT),
                stylesheet_file=str(XSLT_COMPILE),
                output_file=str(VALIDATOR_OUTPUT),
            )

        print(
            f"--- Step 4: Validate XML using the generated XSLT for ALL ECR files in {ECR_FOLDER}",
        )
        print(f"and save reports to {OUTPUT_FOLDER} ---")
        for ecr_file_path in ECR_FOLDER.glob("*.xml"):
            output_file = OUTPUT_FOLDER / f"{ecr_file_path.stem}_validation_report.svrl"
            # Step 4: Apply the generated XSLT to the source XML
            xsltproc.transform_to_file(
                source_file=str(ecr_file_path),
                stylesheet_file=str(VALIDATOR_OUTPUT),
                output_file=str(output_file),
            )
            print(f"--- Validation complete. Report saved to {output_file}")

        print("--- Validation complete process complete for all ECR files. ---")

        # Optional: Read and print the SVRL report for command line visibility
        # print("--- SVRL Validation Report ---")
        # report_path = OUTPUT_FOLDER / "validation_report.svrl"
        # with report_path.open() as report_file:
        #     print(report_file.read())

except Exception as e:  # noqa: BLE001
    print(f"An error occurred during validation: {e}")
