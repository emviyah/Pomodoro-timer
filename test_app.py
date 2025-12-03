
from app import format_time, is_valid_task

def test_format_time():
    assert format_time(0) == "00:00"
    assert format_time(60) == "01:00"
    assert format_time(125) == "02:05"
    assert format_time(25 * 60) == "25:00"

def test_format_time_edge_cases():
    assert format_time(0) == "00:00"      #zero
    assert format_time(59) == "00:59"    #under 1 min
    assert format_time(60) == "01:00"   #exact minute
    assert format_time(3599) == "59:59"  #max for 2-digit mins
    assert format_time(3600) == "60:00"  #1 hour

def test_is_valid_task():
    assert is_valid_task("Buy milk") == True
    assert is_valid_task("  Code Pomodoro!  ") == True
    assert is_valid_task("") == False
    assert is_valid_task("   ") == False
    assert is_valid_task("\t\n") == False