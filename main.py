from pathlib import Path

from saxonche import PySaxonProcessor

CURRENT_DIR = Path(__file__).parent


eicr_file = CURRENT_DIR / "schematron" / "eicr_covid.xml"
schema_file = CURRENT_DIR / "schematron" / "APHL_TextToCodeSchematron_09252025.sch"
xsl = CURRENT_DIR / "schematron" / "iso_svrl_for_xslt2.xsl"

# Define paths to the necessary schxslt stylesheets
include_xsl = CURRENT_DIR / "schematron" / "include.xsl"
expand_xsl = CURRENT_DIR / "schematron" / "expand.xsl"
compile_xsl = CURRENT_DIR / "schematron" / "compile-for-svrl.xsl"

# Temporary files for intermediate steps
stage1_sch = CURRENT_DIR / "schematron" / "stage1.sch.tmp"
stage2_sch = CURRENT_DIR / "schematron" / "stage2.sch.tmp"
validator_xsl = CURRENT_DIR / "schematron" / "validator.xsl.tmp"
svrl_report = CURRENT_DIR / "schematron" / "validation_report.svrl"

try:
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()

        print(f"--- Step 1: Include (using {include_xsl})")
        # Set a custom URIResolver to handle the voc.xml file reference in the schema if needed.
        # The 'document()' function in the schema handles relative paths by default in most cases.

        # Step 1: Process includes
        # Note: For schxslt, you typically apply the XSLT to the SCH file as the source
        xsltproc.transform_to_file(
            source_file=schema_file,
            stylesheet_file=include_xsl,
            output_file=stage1_sch,
        )

        print(f"--- Step 2: Expand (using {expand_xsl})")
        # Step 2: Expand abstract rules
        # No parameters needed here for the basic example
        xsltproc.transform_to_file(
            source_file=stage1_sch,
            stylesheet_file=expand_xsl,
            output_file=stage2_sch,
        )

        print(f"--- Step 3: Compile to XSLT (using {compile_xsl})")
        # Step 3: Compile to an SVRL-producing XSLT stylesheet
        # Pass the vocabulary file path as a parameter if the schema/xsl expects it.
        # In my_schema.sch, it uses document('voc.xml'), so it resolves automatically.
        xsltproc.transform_to_file(
            source_file=stage2_sch,
            stylesheet_file=compile_xsl,
            output_file=validator_xsl,
        )

        print(f"--- Step 4: Validate XML (using {eicr_file} and {validator_xsl})")
        # Step 4: Apply the generated XSLT to the source XML
        xsltproc.transform_to_file(
            source_file=eicr_file,
            stylesheet_file=validator_xsl,
            output_file=svrl_report,
        )

        print(f"--- Validation complete. Report saved to {svrl_report}")

        # Optional: Read and print the SVRL report for command line visibility
        with Path.open(svrl_report, "r", encoding="utf-8") as f:
            print("\n--- SVRL Report ---")
            print(f.read())

except Exception as e:  # noqa: BLE001
    print(f"An error occurred during validation: {e}")


# sct_doc = etree.parse(schema_file)
# schematron = isoschematron.Schematron(sct_doc, store_report=True)

# doc = etree.parse(eicr_file)
# is_valid = schematron.validate(doc)
# report = schematron.validation_report

# if is_valid:
#     print(" VALID EICR")
# else:
#     print(etree.tostring(report, pretty_print=True).decode())


# parser = etree.XMLParser()
# # parser.resolvers.add(FileResolver())

# schematron_doc = etree.parse(schema_file, parser)
# iso_xslt = etree.parse(xsl, parser)
# transform = etree.XSLT(iso_xslt)
# validator_xslt = transform(schematron_doc)

# validator = etree.XSLT(validator_xslt)
# ccda_doc = etree.parse(eicr_file, parser)

# result = validator(ccda_doc)

# result.write("./output.xml", pretty_print=True)
