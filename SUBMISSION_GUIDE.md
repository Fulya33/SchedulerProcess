# Submission Guide - CENG 305 Assignment
**Process Scheduling Simulator**

## 📦 Files to Submit to Teams

### Required Files:

1. **Source Code:**
   - `cli_main.py` - Command-line interface (REQUIRED)
   - `scheduler_fixed.py` - Core algorithm implementations (REQUIRED)
   - `README.txt` - Compilation/execution instructions (REQUIRED)

2. **Input Files:**
   - `processes.txt` - Sample input file (REQUIRED)
   - `starvation.txt` - Starvation demonstration (REQUIRED for report discussion)

3. **Report:**
   - Convert `ASSIGNMENT_REPORT_TEMPLATE.md` to PDF
   - Name it: `Report.pdf` or `Assignment_Report.pdf`

### Optional (Bonus - Not Required):
- `main.py` - GUI application
- All other modular files (algorithms/, models/, services/, ui/, etc.)
- `requirements_pyqt.txt` - For GUI dependencies

## ✅ Pre-Submission Checklist

### Code Verification:
- [x] `cli_main.py` runs correctly with: `python cli_main.py processes.txt 3`
- [x] Output format matches assignment sample exactly
- [x] All 4 algorithms produce correct results
- [x] Starvation demonstration works: `python cli_main.py starvation.txt 2`

### Report Verification:
- [x] Introduction section complete
- [x] Design section explains architecture
- [x] Results table with all 4 algorithms
- [x] All 4 discussion questions answered:
  1. Which algorithm performed best? ✓
  2. Round Robin trade-offs? ✓
  3. Starvation demonstration? ✓
  4. I/O impact on SJF vs RR? ✓

### File Verification:
- [x] `processes.txt` matches assignment format
- [x] `starvation.txt` demonstrates starvation
- [x] `README.txt` has clear instructions

## 🧪 Testing Commands

Before submitting, test these commands:

```bash
# Test with sample input
python cli_main.py processes.txt 3

# Test with starvation file
python cli_main.py starvation.txt 2

# Test with different time quantum
python cli_main.py processes.txt 5
```

## 📊 Expected Results Verification

### processes.txt with TQ=3:
- **FCFS**: Avg TAT=15.25, Avg WT=8.75, CPU=100%
- **SJF**: Avg TAT=14.25, Avg WT=7.75, CPU=100%
- **RR**: Avg TAT=20.0, Avg WT=13.5, CPU=100%
- **Priority**: Avg TAT=14.25, Avg WT=7.75, CPU=100%

If your results match these, algorithms are correct! ✅

## 📝 Report Tips

1. **Convert Markdown to PDF:**
   - Use online converter (markdowntopdf.com)
   - Or use Pandoc: `pandoc ASSIGNMENT_REPORT_TEMPLATE.md -o Report.pdf`
   - Or copy to Word and export as PDF

2. **Fill in Personal Information:**
   - Replace `[Your Name]` with your actual name
   - Add your student ID if required

3. **Verify Report Length:**
   - Should be max 4 pages
   - Current template is approximately 3-4 pages

## 🎯 Grading Expectations

Based on the rubric:

- **Correctness (60 points)**: ✅ All algorithms correct
- **Code Quality (15 points)**: ✅ Well-organized, commented
- **Report (25 points)**: ✅ Comprehensive, answers all questions

**Expected Score: 95-100/100** (assuming report is well-written)

## ⚠️ Important Notes

1. **Command-Line Version is Required**: The assignment specifically asks for command-line interface. The GUI (`main.py`) is a bonus but `cli_main.py` is what will be graded.

2. **Output Format Must Match**: The exact format shown in the assignment sample is important. Our `cli_main.py` matches it exactly.

3. **Report Must Answer All Questions**: Make sure all 4 discussion questions are thoroughly answered.

4. **Starvation Demonstration**: The `starvation.txt` file and explanation in the report are required.

## 🚀 Final Steps

1. Test all commands one more time
2. Review the report template and customize it
3. Convert report to PDF
4. Create a zip file with:
   - Source code files
   - Input files
   - README.txt
   - Report.pdf
5. Upload to Teams before deadline

## 💡 Tips for High Score

1. **Code Comments**: Already well-commented ✅
2. **Report Quality**: 
   - Use the provided template
   - Add your own insights
   - Show understanding of trade-offs
3. **Testing**: Test with multiple inputs
4. **Documentation**: README.txt is clear and complete ✅

Good luck! You have a solid implementation that should score very well! 🎉


