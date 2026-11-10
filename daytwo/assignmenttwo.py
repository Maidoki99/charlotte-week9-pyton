observations = [
    {"well_id": "WELL-01", "field": "Brent", "pressure": 2500.5},
    {"well_id": "WELL-02", "field": "Ninian", "pressure": 2750.0},
    {"well_id": "WELL-07", "field": "Forties", "pressure": 3100.2},
    {"well_id": "WELL-07", "field": "Forties", "pressure": 3050.8},  # Duplicate well
    {"well_id": "WELL-03", "field": "Brent", "pressure": 2400.0},
    {"well_id": "WELL-08", "field": "Ninian", "pressure": 2900.1},
    {"well_id": "WELL-08", "field": "Ninian", "pressure": 2850.4},  # Duplicate well
    {"well_id": "WELL-04", "field": "Piper", "pressure": 2650.3}
]

# ---------------------------------------------------------------------
# Task 1: Print the two earliest observations and the last observation
# ---------------------------------------------------------------------
print("--- Task 1: Earliest and Last Observations ---")

# Using slicing [0:2] to get the first two records (earliest)
earliest_two = observations[0:2]

# Using negative indexing [-1] to get the very last record
last_observation = observations[-1]

# Displaying the results clearly
print("The two earliest observations are:")
for obs in earliest_two:
    print(obs)

print("\nThe last observation is:")
print(last_observation)
print("-" * 40)
# Create empty sets to hold our unique values (like you did in class)
distinct_wells = set()
distinct_fields = set()

# Loop through every observation dictionary in our list
for obs in observations:
    # Use the dictionary keys to read the well_id and field values
    distinct_wells.add(obs["well_id"])
    distinct_fields.add(obs["field"])

# Use the built-in sorted() function to sort them alphabetically
sorted_wells = sorted(distinct_wells)
sorted_fields = sorted(distinct_fields)

# Display the final sorted lists
print("Sorted Distinct Well IDs:", sorted_wells)
print("Sorted Distinct Fields: ", sorted_fields)
print("-" * 40)

print("\n--- Task 3: Pressure Calculations ---")

# Initialize total accumulator and count tracker
total_pressure = 0.0
total_observations = len(observations)

# Loop through each dictionary to accumulate the pressure values
for obs in observations:
    total_pressure += obs["pressure"]

# Calculate the mean (average) by dividing sum by count
mean_pressure = total_pressure / total_observations

# Display the values clearly and label them with 'psi'
print(f"Total Pressure: {total_pressure:.2f} psi")
print(f"Mean Pressure:  {mean_pressure:.2f} psi")
print("-" * 40)

print("\n--- Task 4: Observations Counter per Well ---")

# Initialize an empty dictionary to hold the counts
well_counts = {}

for obs in observations:
    well = obs["well_id"]
    
    # If the well already exists as a key, add 1 to its current count
    if well in well_counts:
        well_counts[well] += 1
    # If it is a new well we haven't seen yet, initialize its count to 1
    else:
        well_counts[well] = 1

# Display the final counts dictionary
print("Observation counts per well dictionary:")
print(well_counts)

# (Task 5 requirement: Add meaningful comments, sensible variable names and readable output)
print("\nReadable breakdowns per well:")
for well, count in well_counts.items():
    print(f"  Well {well} has {count} observation(s).")
print("-" * 40)
"""
Using a list of dictionaries is highly advantageous for data tracking 
because a standard Python dictionary requires completely unique keys. 
If we were to use a single dictionary where the well IDs served as the 
primary keys, any subsequent observation sharing an identical well ID 
(such as the duplicate entries for WELL-07 and WELL-08) would completely 
overwrite the previous data point. This would result in an immediate 
loss of historical data and sequential readings.

By contrast, an outer list preserves chronological order and allows 
duplicate records to coexist seamlessly. Each separate observation is 
contained within its own independent dictionary block inside the list. 
This structure ensures that every single data point is fully preserved 
for accurate calculations.
"""