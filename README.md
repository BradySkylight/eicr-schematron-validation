# eICR Validator
## Summary
We have been provided a schematron file that is used by APHL for eICR validation.  Our goal in leveraging this file is to be able to produce expected schematron validation output based upon test/sample eICR messages.  We can then leverage the errors and the eICR messages to validate our functionality to find proper codes and augment them.  Then our team can leverage the same validator, using the provided schematron file, to ensure that our augmented eICR messages meet all requirements.

## Dependencies

- [Saxonc-he](https://pypi.org/project/saxonche/)
- [XSLT Files](https://codeberg.org/SchXslt/schxslt/releases/download/v1.10.1/schxslt-1.10.1-xslt-only.zip)
   - Download the zip
   - Extract it locally
   - Copy the `2.0` folder into the `schxslt` folder in this repo/project
- This project uses the [APHL schematron file](./eicr-validator/schematron/) and APHL voc.xml files for validation.  These have been added to this project in the `schematron` folder.  If there are any changes/updates to the APHL validation for TTC these files may need to be updated.


## Schematron Output

The output from this validator is not in the expected format for TTC functionality.  There is more work to do to translate the report.svrl file(s) into the proper XML format that TTC expects from APHL Schematron Error Output.  However, for now this tool can suffice as a validation tool.

I am using the provided APHL Schematron to validate various eICR messages that are samples provided by [AIMs](https://ecr.aimsplatform.org/ehr-implementers/test-package.php).  Some of the messages have been modified to produce errors during validation, while others have not been modified to demonstrate what a valid eICR looks like. A sampling of what the output errors, related to our work, look like:


## Execution

- Add any eICR files to the `eicr` folder in the project
- Then just `Run` the main.py file via terminal (so you can see the output during the process)
   - You will see the progress of the process
   - The resulting validation report files will be stored in the `output` folder

**NOTE: if any changes are made to the Schematron file or any of the schxslt files steps 1-3 should be rerun!  This can be done by removing the files in the `output` folder and running the process list above**