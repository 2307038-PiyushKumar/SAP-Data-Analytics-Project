# 📦 SAP Inventory & Supply Chain Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly)
![Dash](https://img.shields.io/badge/Dash-Interactive%20Dashboard-008DE4)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end **inventory and supply chain analytics solution** built with Python, Pandas, Plotly, and Dash. It reads SAP-style CSV exports (Inventory, Suppliers, Warehouses), performs multi-dimensional analysis, generates static chart exports, and serves an interactive web dashboard with real-time filters.

---

## 📁 Project Structure

```
SAP_Dashboard/
├── Data/
│   ├── Inventory.csv          # Transaction-level stock records
│   ├── Suppliers.csv          # Supplier master with ratings & on-time %
│   └── Warehouses.csv         # Warehouse capacity data
├── Scripts/
│   ├── analysis.py            # Batch analysis → saves charts + CSVs to Output/
│   └── dashboard.py           # Interactive Dash web app
├── Output/                    # Auto-created — charts & summary CSVs land here
├── requirements.txt
└── README.md
```

---

## 📊 Features

### `analysis.py` — Static Analysis & Exports
| # | Analysis | Output File |
|---|----------|-------------|
| 1 | Average stock level by product category | `stock_by_category_chart.png` |
| 2 | Top 10 slow-moving items by locked-up value | `slow_moving_chart.png` + `slow_moving_items.csv` |
| 3 | Stock movement type distribution (donut chart) | `movement_distribution_chart.png` |
| 4 | Monthly inbound vs outbound trend | `monthly_movement_chart.png` |
| 5 | Supplier rating vs on-time delivery % (bubble chart) | `supplier_performance_chart.png` + `supplier_performance.csv` |
| 6 | Warehouse utilisation % vs capacity | `warehouse_utilisation_chart.png` |
| 7 | KPI summary (10 headline metrics) | `kpi_summary.csv` |

### `dashboard.py` — Interactive Web Dashboard
- **Filters:** Category · Warehouse · Movement Type · Date Range
- **KPI cards:** Live-updating headline metrics
- **6 interactive charts** powered by Plotly
- **Transaction log table** with slow-moving row highlighting
- Dark-themed UI (Dash Bootstrap CYBORG theme)

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/your-username/sap-supply-chain-dashboard.git
cd sap-supply-chain-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your data files
Place your CSV files in the `Data/` folder:
```
Data/
├── Inventory.csv
├── Suppliers.csv
└── Warehouses.csv
```

---

## ▶️ Running the Project

### Run static analysis (generates charts & CSVs)
```bash
cd Scripts
python analysis.py
```
Outputs are saved to the `Output/` folder.

### Launch the interactive dashboard
```bash
cd Scripts
python dashboard.py
```
Then open your browser at: **[http://127.0.0.1:8050](http://127.0.0.1:8050)**

Press `Ctrl+C` in the terminal to stop the server.

---

## 📋 Data Schema

### `Inventory.csv`
| Column | Description |
|--------|-------------|
| `TransactionID` | Unique transaction identifier |
| `ProductID` / `ProductName` | Product reference |
| `Category` | Product category |
| `WarehouseID` | Warehouse reference |
| `SupplierID` | Supplier reference |
| `Date` | Transaction date |
| `Quantity` | Units moved |
| `UnitPrice` / `TotalValue` | Pricing fields |
| `MovementType` | Inbound / Outbound / Transfer / Adjustment |
| `StockLevel` | Current stock on hand |
| `ReorderPoint` | Minimum stock threshold |
| `SlowMoving` | Yes / No flag |

### `Suppliers.csv`
| Column | Description |
|--------|-------------|
| `SupplierID` | Unique supplier ID |
| `SupplierName` | Supplier name |
| `Rating` | Performance rating (1–5) |
| `OnTime_Pct` | On-time delivery percentage |

### `Warehouses.csv`
| Column | Description |
|--------|-------------|
| `WarehouseID` | Unique warehouse ID |
| `WarehouseName` | Warehouse name |
| `Capacity_Units` | Maximum storage capacity |

---

## 📦 Dependencies

```
pandas
plotly
dash
dash-bootstrap-components
kaleido
```

Install all at once:
```bash
pip install -r requirements.txt
```

> **Note:** `kaleido` is required by Plotly to export static `.png` chart images in `analysis.py`.

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FileNotFoundError` for CSVs | Ensure CSVs are in the `Data/` folder |
| Port 8050 already in use | Change to `app.run(port=8051)` in `dashboard.py` |
| `kaleido` PNG export fails | Run `pip install kaleido --upgrade` |
| Blank charts in dashboard | Check that your filter combination returns data |

---

## 🚀 Future Enhancements

- [ ] Export dashboard charts as PDF report
- [ ] Add forecasting module (Prophet / ARIMA) for stock prediction
- [ ] Connect to live SAP BW/4HANA via REST API
- [ ] Role-based access with authentication
- [ ] Deploy to cloud (AWS / Azure / GCP)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -m 'Add new analysis'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ using Python · Pandas · Plotly · Dash
