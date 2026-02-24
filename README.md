# eICR Validator
## Summary
We have been provided a schematron file that is used by APHL for eICR validation.  Our goal in leveraging this file is to be able to produce expected schematron validation output based upon test/sample eICR messages.  We can then leverage the errors and the eICR messages to validate our functionality to find proper codes and augment them.  Then our team can leverage the same validator, using the provided schematron file, to ensure that our augmented eICR messages meet all requirements.

## Dependencies

from saxonche import PySaxonProcessor

https://codeberg.org/SchXslt/schxslt/releases/download/v1.10.1/schxslt-1.10.1-xslt-only.zip

APHL schematron file

includes voc_ttc.xml



## Schematron Output
While we will not know for certain what the XPaths given by APHL will look like until we get more information from them, we can run Schematron ourselves to get an idea of what it may look like. Setting up and running Schematron is a fairly annoying process, but if you are interested, here is the repo with the code I used.

I am using the provided APHL Schematron to validate various eICR messages that are samples provided by [AIMs](https://ecr.aimsplatform.org/ehr-implementers/test-package.php).  Some of the messages have been modified to produce errors during validation, while others have not been modified to demonstrate what a valid eICR looks like. A sampling of what the output errors, related to our work, look like:

```xml
<Results xmlns="urn:gov:nist:cdaGuideValidator">
        <validationResult xmlns="">
            <issue severity="errors">
                <message>Text to Code: Lab Test Name Resulted does not have a @code attribute</message>
                <context>/ClinicalDocument/component[1]/structuredBody[1]/component[5]/section[1]/entry[1]/organizer[1]/component[1]/observation[1]</context>
                <test> not(cda:code) or cda:code/@code or cda:code/cda:translation/@code</test>
                <specification/>
            </issue>
        </validationResult>
        <validationResult xmlns="">
            <issue severity="errors">
                <message>Text to Code: Lab Test Name Resulted code and translation data elements @codeSystem attribute are not LOINC 2.16.840.1.113883.6.1</message>
                <context>/ClinicalDocument/component[1]/structuredBody[1]/component[6]/section[1]/entry[1]/organizer[1]/component[1]/observation[1]</context>
                <test>not(cda:code/@code or cda:code/cda:translation/@code) or cda:code[@codeSystem = '2.16.840.1.113883.6.1'] or cda:code/cda:translation[@codeSystem = '2.16.840.1.113883.6.1']</test>
                <specification/>
            </issue>
        </validationResult>
    </Results>
```