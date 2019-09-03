#!/usr/bin env python3
import SolvisRemoteFetcher as srf

def test_fulldata():
    data = 'AA5555AA056B101A3103401A00B402B401D301A3025E023002A2FE8B028D02BE0046011001C409AE01C409C40900000000000000000000004C4C0D0000000000000000640000000000000000000000BA60114DFFFF4E46BCC6010001010101000002010101009674000000130903349000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    # solvis Header="AA5555AA056B",Uhrzeit="2019-09-03 16:26:49",Anlagentyp="0340",Systemnummer="1A00",S1=69.2,S2=43.6,S3=46.7,S4=67.5,S5=60.6,S6=56.0,S7=-35.0,S8=65.1,S9=65.3,S10=19.0,S11=32.6,S12=27.2,S13=250.0,S14=43.0,S15=250.0,S16=250.0,S18=0.0,S17=0i,AI1=0.0,AI2=0.0,AI3=0.0,P1=False,P2=True,P3=True,P4=True,RF1=0.0,RF2=0.0,RF3=0.0,A1=False,A2=False,A3=True,A4=False,A5=False,A6=False,A7=False,A8=False,A9=False,A10=False,A11=False,A12=False,A13=False,A14=False,skip_1="BA60114DFFFF4E46",SEv=50876i,skip_2="0100010101",P5v=True,skip_3="000002010101009674",SLv=0.0 1567513560'

    sr = srf.SolvisRemote()
    sr.parseValues(data)

    # Sensor data
    assert sr.values['S1'] == 69.2
    assert sr.values['S2'] == 43.6
    assert sr.values['S3'] == 46.7
    assert sr.values['S4'] == 67.5
    assert sr.values['S5'] == 60.6
    assert sr.values['S6'] == 56.0
    assert sr.values['S7'] == -35.0
    assert sr.values['S8'] == 65.1
    assert sr.values['S9'] == 65.3
    assert sr.values['S10'] == 19.0
    assert sr.values['S11'] == 32.6
    assert sr.values['S12'] == 27.2
    assert sr.values['S13'] == 250.0
    assert sr.values['S14'] == 43.0
    assert sr.values['S15'] == 250.0
    assert sr.values['S16'] == 250.0
    assert sr.values['S17'] == 0
    assert sr.values['S18'] == 0.0

    # Relais data
    assert sr.values['A1'] == False
    assert sr.values['A2'] == False
    assert sr.values['A3'] == True
    assert sr.values['A4'] == False
    assert sr.values['A5'] == False
    assert sr.values['A6'] == False
    assert sr.values['A7'] == False
    assert sr.values['A8'] == False
    assert sr.values['A9'] == False
    assert sr.values['A10'] == False
    assert sr.values['A11'] == False
    assert sr.values['A12'] == False
    assert sr.values['A13'] == False
    assert sr.values['A14'] == False


def test_sensors2():
    data = 'AA5555AA056B10193B03401A00B402B501D401A30269023602A2FE89028D02C00046011001C409AD01C409C40900000000000000000000004C4C0D0000000000000000640000000000000000000000BA60114DFFFF4E46BCC6010001010101000002010101009674000000130903112600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    # solvis Header="AA5555AA056B",Uhrzeit="2019-09-03 16:25:59",Anlagentyp="0340",Systemnummer="1A00",S1=69.2,S2=43.7,S3=46.8,S4=67.5,S5=61.7,S6=56.6,S7=-35.0,S8=64.9,S9=65.3,S10=19.2,S11=32.6,S12=27.2,S13=250.0,S14=42.9,S15=250.0,S16=250.0,S18=0.0,S17=0i,AI1=0.0,AI2=0.0,AI3=0.0,P1=False,P2=True,P3=True,P4=True,RF1=0.0,RF2=0.0,RF3=0.0,A1=False,A2=False,A3=True,A4=False,A5=False,A6=False,A7=False,A8=False,A9=False,A10=False,A11=False,A12=False,A13=False,A14=False,skip_1="BA60114DFFFF4E46",SEv=50876i,skip_2="0100010101",P5v=True,skip_3="000002010101009674",SLv=0.0 1567513510'

    sr = srf.SolvisRemote()
    sr.parseValues(data)
    assert sr.values['S1'] == 69.2
    assert sr.values['S10'] == 19.2
    assert sr.values['S12'] == 27.2

