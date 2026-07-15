import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# Tax function
# =====================================================================

# Gets a gross amount and returns the net amount accounrding to 2026 SKAT rules (can be replaced with any tax function)
def skat(g):
    if g <= 0:
        return 0
        
    # 1. Labor Market Contribution (AM-bidrag)
    am_rate = 0.08  # 8% standard flat rate
    am_bidrag = g * am_rate
    salary_after_am = g - am_bidrag  # Key basis for individual taxes
    
    # 2. Automatically granted 2026 tax deductions (Fradrag)
    # Employment deduction (Beskæftigelsesfradrag): 12.75% capped at 63,300 DKK
    beskaeftigelses_fradrag = min(salary_after_am * 0.1275, 63_300)
    
    # Job deduction (Jobfradrag): 4.5% of salary exceeding 235,200 DKK, capped at 3,100 DKK
    job_fradrag = 0.0
    if g > 235_200:
        job_fradrag = min((g - 235_200) * 0.045, 3_100)
        
    # Personal Allowance (Personfradrag)
    person_fradrag = 54_100
    
    # Deductions lower taxable salary base but do NOT reduce AM-bidrag
    total_allowances = beskaeftigelses_fradrag + job_fradrag + person_fradrag
    taxable_salary = max(0.0, salary_after_am - total_allowances)
    
    # 3. Base Taxes (Bundskat & Municipal Tax)
    bundskat_rate = 0.1201  # 12.01%
    kommuneskat_rate = 0.2339  # 23.39% (2026 rate for Copenhagen)
    base_tax_rate = bundskat_rate + kommuneskat_rate
    
    total_tax = taxable_salary * base_tax_rate
    
    # 4. Progressive Reform Brackets (Calculated on salary_after_am)
    # Middle tax (Mellemskat): 7.5% on salary between 641,200 DKK and 777,900 DKK
    if salary_after_am > 641_200:
        mellemskat_taxable = min(salary_after_am, 777_900) - 641_200
        total_tax += mellemskat_taxable * 0.075
        
    # Top tax (Topskat): 7.5% on salary between 777,900 DKK and 2,592,700 DKK
    if salary_after_am > 777_900:
        topskat_taxable = min(salary_after_am, 2_592_700) - 777_900
        total_tax += topskat_taxable * 0.075
        
    # Top-Top tax (Toptopskat): 5.0% on salary exceeding 2,592,700 DKK
    if salary_after_am > 2_592_700:
        toptopskat_taxable = salary_after_am - 2_592_700
        total_tax += toptopskat_taxable * 0.05
        
    # Net salary
    net_amount = salary_after_am - total_tax
    return round(net_amount, 2)

# =====================================================================
# Analysis
# =====================================================================

# Gross yearly salary (DKK)
g = 900_000
# Net yearly salary (DKK)
n = skat(g)
# Number of working days per week [0,5]
x = 5

print("Full-time percentual net wrt gross yearly salary: " + str(n / g * 100) + " %")

# Gross yearly salary retained taking into account part-time (absolute and percentual wrt full-time)
g_r = lambda x : x/5 * g
g_r_perc = lambda x: g_r(x) / g

# Net yearly salary retained taking into account part-time (absolute and percentual wrt full-time)
n_r = lambda x : skat(g_r(x))
n_r_perc = lambda x : n_r(x) / n

# Find x to maximize percentual premium retention defined as
p_r_perc = lambda x : n_r_perc(x) - g_r_perc(x)

# =====================================================================
# Plots
# =====================================================================

# Danish salary tax: gross vs. net salary (Copenhagen 2026)

# Expanded range of gross salary values to cross into the toptopskat bracket
gross_axis = np.linspace(0, 3_200_000, 2000)
net_values = np.array([skat(g) for g in gross_axis])

# Exact mathematical gross coordinates for the bracket entries
mellemskat_gross = 641_200 / 0.92
topskat_gross = 777_900 / 0.92
toptopskat_gross = 2_592_700 / 0.92

# Initialize the plot
plt.figure(figsize=(12, 7))

# Plot gross salary vs Net salary
plt.plot(gross_axis, net_values, label='Net salary (n)', color='#2ca02c', linewidth=2.5)

# Plot gross salary vs itself as a reference line (un-taxed salary baseline)
plt.plot(gross_axis, gross_axis, label='Gross salary (g) / Untaxed baseline', color='#d62728', linestyle='--', linewidth=1.5)

# Add visual indicators for the 2026 progressive bracket entries
plt.axvline(x=mellemskat_gross, color='#1f77b4', linestyle=':', alpha=0.7, label='Mellemskat bracket entry (~697k gross)')
plt.axvline(x=topskat_gross, color='#9467bd', linestyle=':', alpha=0.7, label='Topskat bracket entry (~845k gross)')
plt.axvline(x=toptopskat_gross, color='#e377c2', linestyle=':', alpha=0.7, label='Toptopskat bracket entry (~2.82M gross)')

# Text annotations displaying the exact percentage of taxes taken in each range (marginal tax rates)
plt.text(350_000, skat(350_000) + 120000, 'Tax: ~34.8%\n(Base taxes + AM-bidrag)', fontsize=9, color="#ff7f0e", weight='bold', ha='center')
plt.text(770_000, skat(770_000) + 120000, 'Tax: ~42.3%\n(mellemskat)', fontsize=9, color='#ff7f0e', weight='bold', ha='center')
plt.text(1_700_000, skat(1_700_000) + 120000, 'Tax: ~49.8%\n(topskat)', fontsize=9, color='#ff7f0e', weight='bold', ha='center')
plt.text(2_950_000, skat(2_950_000) + 120000, 'Tax: ~54.8%\n(toptopskat)', fontsize=9, color='#ff7f0e', weight='bold', ha='center')

# Aesthetics and formatting
plt.title('Danish salary tax: gross vs. net salary (Copenhagen 2026)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Gross yearly salary (DKK)', fontsize=12)
plt.ylabel('Net yearly salary (DKK)', fontsize=12)

# Format axes numbers with commas for thousands
plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda y, loc: f"{int(y):,}"))

plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

# Render the plot
plt.show()

# Part-time tax efficiency: premium retention (%) (Copenhagen 2026)

# Define relevant gross salary bands to analyze, mapping the entry and ceiling of each bracket
salary_bands = {
    'Example below mellemskat entry': 500_000 / 0.92,
    'Mellemskat entry': 641_200 / 0.92,
    'Topskat entry': 777_900 / 0.92,
    'Toptopskat entry': 2_592_700 / 0.92,
    'Example gross yearly salary': g,
}

# Setup a 2x3 subplot layout grid window to fit all 5 plots cleanly
fig, axes = plt.subplots(2, 3, figsize=(20, 10))
axes = axes.flatten()

# Sample range of working days from 0 to 5
days_axis = np.linspace(0, 5, 1000)

# Iterate across each individual salary band boundary to build the matrix
for idx, (title, g_val) in enumerate(salary_bands.items()):
    
    # Temporarily override the existing global variables for the current loop iteration
    g = g_val
    n = skat(g)
    
    # Map out percentual premium curve vector using the existing p_r_perc function
    perc_premium_values = np.array([p_r_perc(val) * 100 for val in days_axis])
    
    # Identify maximum position
    optimal_index = np.argmax(perc_premium_values)
    optimal_x = days_axis[optimal_index]
    max_premium = perc_premium_values[optimal_index]
    
    # Plot array data
    ax = axes[idx]
    ax.plot(days_axis, perc_premium_values, color='#1f77b4', linewidth=2)
    
    # Add peak value indicator markers
    ax.plot(optimal_x, max_premium, 'ro', label=f'Peak: {max_premium:+.2f}% at {optimal_x:.2f} days')
    
    # Calculate relevant tax bracket limits transitioned into working day coordinates
    # g : 5 = band_entry / 0.92 : x
    # x = 5 * (band_entry / 0.92 / g)
    mellemskat_entry_x = 5 * (641_200 / 0.92 / g) 
    topskat_entry_x = 5 * (777_900 / 0.92 / g)
    toptopskat_entry_x = 5 * (2_592_700 / 0.92 / g)
   
    # Plot bracket entry lines consistently if they fall within the current part-time week frame (0 < x < 5)
    if 0 < mellemskat_entry_x < 5:
        ax.axvline(x=mellemskat_entry_x, color='#1f77b4', linestyle='--', alpha=0.5, label='Mellemskat entry')
        
    if 0 < topskat_entry_x < 5:
        ax.axvline(x=topskat_entry_x, color='#9467bd', linestyle='--', alpha=0.5, label='Topskat entry')
        
    if 0 < toptopskat_entry_x < 5:
        ax.axvline(x=toptopskat_entry_x, color='#e377c2', linestyle='--', alpha=0.5, label='Toptopskat entry')

    # Context styling and metadata matching formatting choices
    ax.set_title(f"{title}\n(g = {int(g_val):,} DKK)", fontsize=10, fontweight='bold')
    ax.set_xlabel('Working days per week (x)', fontsize=9)
    ax.set_ylabel('Premium retention (%)', fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, loc: f"{y:+.1f}%"))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower center', fontsize=8)

# Hide the unused 6th subplot axis in the 2x3 grid layout frame
axes[-1].axis('off')

# Universal aesthetics configuration
plt.suptitle('Part-time tax efficiency: premium retention (%) (Copenhagen 2026)', fontsize=14, fontweight='bold', y=0.97)
plt.tight_layout(rect=[0, 0.03, 1, 0.94])

# Render the layout grid window
plt.show()