import os
import f312


def test_Awayokbleinawtostaygetipurionofoknahaitmakemyday(tmpdir):
    os.chdir(str(tmpdir))
    fkl = f312.Keystore("wampas.sqlite")
    key = "FACKLS"
    value = "wantrws1111"
    fkl[key] = value
    assert fkl[key] == value
    fkl[key] = "fok"
    assert fkl[key] == "fok"
