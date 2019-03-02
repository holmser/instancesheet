# AWS Instance Availability Spreadsheet Generator

This is a quick-and-dirty script to generate a spreadsheet populated with instance types available in each region as exposed by the pricing API.  It is sloppy and incomplete. Currently only linux instance types are displayed with no pre-installed software (no SQL Server, etc).  **Data has been spot checked but has not been thoroughly verified to be correct.  Use at your own risk.**

![Spreadsheet Image](/images/example.png)

## Usage

```sh
pip install -r requirements.txt
python instancesheet.py
# instancesheet.xlsx will be generated in the current directory
```
