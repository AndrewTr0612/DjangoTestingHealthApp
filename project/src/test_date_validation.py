"""
Test script to verify weight entry date validation
"""
from datetime import date, timedelta
from account.forms import WeightEntryForm

print("Testing Weight Entry Date Validation\n")
print("=" * 50)

# Test 1: Today's date (should be valid)
print("\n1. Testing with today's date...")
today_data = {
    'weight_kg': 75.5,
    'recorded_date': date.today(),
    'notes': 'Test entry for today'
}
form1 = WeightEntryForm(data=today_data)
if form1.is_valid():
    print("   ✓ PASS: Today's date is accepted")
else:
    print("   ✗ FAIL: Today's date rejected")
    print(f"   Errors: {form1.errors}")

# Test 2: Past date (should be valid)
print("\n2. Testing with past date (7 days ago)...")
past_date = date.today() - timedelta(days=7)
past_data = {
    'weight_kg': 76.0,
    'recorded_date': past_date,
    'notes': 'Test entry for past date'
}
form2 = WeightEntryForm(data=past_data)
if form2.is_valid():
    print("   ✓ PASS: Past date is accepted")
else:
    print("   ✗ FAIL: Past date rejected")
    print(f"   Errors: {form2.errors}")

# Test 3: Future date (should be invalid)
print("\n3. Testing with future date (tomorrow)...")
future_date = date.today() + timedelta(days=1)
future_data = {
    'weight_kg': 74.5,
    'recorded_date': future_date,
    'notes': 'Test entry for future date'
}
form3 = WeightEntryForm(data=future_data)
if not form3.is_valid() and 'recorded_date' in form3.errors:
    print("   ✓ PASS: Future date is correctly rejected")
    print(f"   Error message: {form3.errors['recorded_date'][0]}")
else:
    print("   ✗ FAIL: Future date was accepted (should be rejected)")

# Test 4: Far future date (should be invalid)
print("\n4. Testing with far future date (30 days ahead)...")
far_future_date = date.today() + timedelta(days=30)
far_future_data = {
    'weight_kg': 73.0,
    'recorded_date': far_future_date,
    'notes': 'Test entry for far future date'
}
form4 = WeightEntryForm(data=far_future_data)
if not form4.is_valid() and 'recorded_date' in form4.errors:
    print("   ✓ PASS: Far future date is correctly rejected")
    print(f"   Error message: {form4.errors['recorded_date'][0]}")
else:
    print("   ✗ FAIL: Far future date was accepted (should be rejected)")

print("\n" + "=" * 50)
print("Validation tests completed!")
