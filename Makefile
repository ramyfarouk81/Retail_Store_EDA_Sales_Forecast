
---

## 2️⃣ `Makefile`

```makefile
# ============================================================
# Makefile — Sales & Distribution Analysis
# Usage: make <target>
# ============================================================

PYTHON  := python
PIP     := pip
JUPYTER := jupyter notebook
DATA    := data/Sales_data.ftr
CLEAN   := data/cleaned_sales_data.csv
PLOTS   := plots
NB      := notebooks/Sales_Analysis.ipynb

.PHONY: help install clean notebook plots export push

help:           ## Show this help menu
	@echo 'Available commands:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:        ## Install Python dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo '✅ Dependencies installed'

notebook:       ## Launch Jupyter Notebook
	$(JUPYTER) $(NB)

plots:          ## Export all plots to plots/ as HTML + PNG
	@mkdir -p $(PLOTS)
	$(PYTHON) src/export_plots.py
	@echo '✅ Plots exported to $(PLOTS)/'

clean:          ## Remove generated plots and caches
	rm -rf $(PLOTS)/*.png $(PLOTS)/*.html
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.ipynb_checkpoints' -exec rm -rf {} +
	@echo '🧹 Cleaned'

clean-data:     ## Delete the cached feather file (forces re-read from Excel)
	rm -f $(DATA)
	@echo '🗑️ Feather cache removed'

push:           ## Commit and push to GitHub
	git add -A
	git commit -m 'Update analysis and plots' || echo 'Nothing to commit'
	git push origin main
	@echo '🚀 Pushed to GitHub'

status:         ## Show git status
	git status