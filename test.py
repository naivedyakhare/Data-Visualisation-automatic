import json

arr = [
    {
        "Variable_Name": "STUDYID",
        "Variable_Label": "Study Identifier",
        "Type": "Char",
        "Derivation": "demo.study_id",
        "example": 101
    },
    {
        "Variable_Name": "DOMAIN",
        "Variable_Label": "Domain Abbreviation",
        "Type": "Char",
        "Derivation": "dm",
        "example": "dm"
    },
    {
        "Variable_Name": "USUBJID",
        "Variable_Label": "Unique Subject Identifier",
        "Type": "Char",
        "Derivation": "demo.study_id + '-' + demo.site_id + '-'  + demo.subjid",
        "example": "101-11-0011"
    },
    {
        "Variable_Name": "SUBJID",
        "Variable_Label": "Subject Identifier for the Study",
        "Type": "Char",
        "Derivation": "demo.subjid",
        "example": "0011"
    },
    {
        "Variable_Name": "RFSTDTC",
        "Variable_Label": "Subject Reference Start Date\/Time",
        "Type": "Char",
        "Derivation": "first expo.exdtc",
        "example": "2020-12-13"
    },
    {
        "Variable_Name": "RFENDTC",
        "Variable_Label": "Subject Reference End Date\/Time",
        "Type": "Char",
        "Derivation": "last expo.exdtc",
        "example": "2020-05-14"
    },
    {
        "Variable_Name": "RFXSTDTC",
        "Variable_Label": "First Date\/Time of Exposure",
        "Type": "Char",
        "Derivation": "first expo.exdtc",
        "example": "2020-12-13"
    },
    {
        "Variable_Name": "RFXENDTC",
        "Variable_Label": "Last Date\/Time of Exposure",
        "Type": "Char",
        "Derivation": "last expo.exdtc",
        "example": "2020-05-14"
    },
    {
        "Variable_Name": "RFICDTC",
        "Variable_Label": "Informed Consent",
        "Type": "Char",
        "Derivation": "desp.cons_dt",
        "example": "2020-12-01"
    },
    {
        "Variable_Name": "REPENDTC",
        "Variable_Label": "Date\/Time of End of Participation",
        "Type": "Char",
        "Derivation": "last date of ( expo.exdtc, desp.ds_dt )",
        "example": "2020-05-24"
    },
    {
        "Variable_Name": "DTHDTC",
        "Variable_Label": "Date\/Time of Death",
        "Type": "Char",
        "Derivation": "desp.death_dt",
        "example": "2020-05-24"
    },
    {
        "Variable_Name": "DTHFL",
        "Variable_Label": "Subject Death Flag",
        "Type": "Char",
        "Derivation": "Y' if desp.death_dt is not missing",
        "example": "Y"
    },
    {
        "Variable_Name": "SITEID",
        "Variable_Label": "Study Site Identifier",
        "Type": "Char",
        "Derivation": "demo.site_id",
        "example": 11
    },
    {
        "Variable_Name": "BRTHDTC",
        "Variable_Label": "Date \/ Time of Birth",
        "Type": "Char",
        "Derivation": "demo.brith_dt",
        "example": "1990-02-22"
    },
    {
        "Variable_Name": "AGE",
        "Variable_Label": "Age",
        "Type": "Num",
        "Derivation": " year of  desp.cons_dt - year of demo.birth_dt ",
        "example": 30
    },
    {
        "Variable_Name": "AGEU",
        "Variable_Label": "Age Units",
        "Type": "Char",
        "Derivation": "YEARS",
        "example": "YEARS"
    },
    {
        "Variable_Name": "SEX",
        "Variable_Label": "Sex",
        "Type": "Char",
        "Derivation": "demo.sex",
        "example": "M"
    },
    {
        "Variable_Name": "RACE",
        "Variable_Label": "Race",
        "Type": "Char",
        "Derivation": "demo.race",
        "example": "WHITE"
    },
    {
        "Variable_Name": "ARMCD",
        "Variable_Label": "Planned Arm Code",
        "Type": "Char",
        "Derivation": "rand.trt_cd",
        "example": "C"
    },
    {
        "Variable_Name": "ARM",
        "Variable_Label": "Description of Planned Arm",
        "Type": "Char",
        "Derivation": "rand.trt",
        "example": "CONTROL"
    },
    {
        "Variable_Name": "ACTARMCD",
        "Variable_Label": "Actual Arm Code",
        "Type": "Char",
        "Derivation": "rand.trt_cd",
        "example": "C"
    },
    {
        "Variable_Name": "ACTARM",
        "Variable_Label": "Description of Actual Arm",
        "Type": "Char",
        "Derivation": "rand.trt",
        "example": "CONTROL"
    },
    {
        "Variable_Name": "ARMNRSN",
        "Variable_Label": "Reason Arm and\/or Actual Arm is Null",
        "Type": "Char",
        "Derivation": "rand.trt_reas",
        "example": "UNPLANNED TREATMENT"
    },
    {
        "Variable_Name": "ACTARMUD",
        "Variable_Label": "Description of Unplanned Actual Arm",
        "Type": "Char",
        "Derivation": "rand.trt_reas2",
        "example": "MISTAKE FROM SITE"
    },
    {
        "Variable_Name": "COUNTRY",
        "Variable_Label": "Country",
        "Type": "Char",
        "Derivation": "USA",
        "example": "USA"
    }
]

d = {}
i = 0
for obj in arr:
    d[f"{i}"] = obj
    i += 1

d = json.dumps(d, indent=4)
# print(d)

with open("file.txt", "w") as f:
    f.write(str(d))
    f.close()
# print(d)