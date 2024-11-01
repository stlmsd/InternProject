from flask import Flask, render_template
import oracledb

app = Flask(__name__)

dsn = oracledb.makedsn("RJMSDDBT02","1521",service_name="gisdevl")
username=" " #Fill with your username
password=" " #Fill with your password

ss_table_names = ["ssManhole", "ssInlet", "ssIntakeOutfall", "ssCleanout", "ssNetworkJunction",
                  "ssNetworkStructure","ssValve", "SSP", "ssPump", "ssPumpStation","ssGhostPipe", 
                  "ssGravityMain", "ssPressurizedMain", "ssCasing"]

sw_table_names = ["swManhole", "swInlet", "swIntakeOutfall", "swCleanout", "swNetworkJunction", 
                  "swNetworkStructure", "swValve", "swPump", "swPumpStation", "swGhostPipe",
                  "swGravityMain", "swPressurizedMain", "swCasing", "swManagementPoint", "swManagementLine"]

def fetch_status_counts(table_name, feature_type):
    query = f"""
        SELECT 
            COUNT(CASE WHEN STATUS = 1 THEN 1 END) AS Active,
            COUNT(CASE WHEN STATUS = 2 THEN 1 END) AS Abandoned,
            COUNT(CASE WHEN STATUS = 3 THEN 1 END) AS Removed,
            COUNT(CASE WHEN STATUS = 4 THEN 1 END) AS Consolidated,
            COUNT(CASE WHEN STATUS = 5 THEN 1 END) AS Design,
            COUNT(CASE WHEN STATUS = 6 THEN 1 END) AS Operating,
            COUNT(CASE WHEN STATUS = 7 THEN 1 END) AS To_Be_Removed,
            COUNT(CASE WHEN STATUS = 8 THEN 1 END) AS Inactive
        FROM MSD.{table_name}
        """

    with oracledb.connect(user=username, password=password, dsn = dsn) as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchone()

        columns = ["Active", "Abandoned", "Removed", "Consolidated", "Design", "Operating", "To_Be_Removed", "Inactive"]

        data = {
            "Feature_Name": table_name,
            "Feature_Type": feature_type,
            **dict(zip(columns, result))}
    return data

# Routes
@app.route('/')
def index():
    
    table_data = []

    # SS Tables
    for index, table_name in enumerate(ss_table_names, start = 1):
        status_counts = fetch_status_counts(table_name, "SS")
        status_counts["S_No"] = index
        table_data.append(status_counts)

    # sw Tables
    for index, table_name in enumerate(sw_table_names, start = 1):
        status_counts = fetch_status_counts(table_name, "SW")
        status_counts["S_No"] = index
        table_data.append(status_counts)

    return render_template('index.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)