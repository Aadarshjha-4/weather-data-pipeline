import mysql.connector
import pandas as pd
from pathlib import Path

connection = None
cursor = None

try:
    # 1. Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="weather_pipeline"
    )

    print("MySQL connected successfully!")

    # 2. EXTRACT: Read raw weather data
    query = """
        SELECT recorded_at, temperature, humidity, wind_speed
        FROM weather_raw
    """

    df = pd.read_sql(query, connection)

    print("\nRaw Weather Data:")
    print(df)

    # 3. TRANSFORM: Clean data
    df = df.dropna(
        subset=[
            "recorded_at",
            "temperature",
            "humidity",
            "wind_speed"
        ]
    )

    df = df.drop_duplicates()

    # Validate weather values
    df = df[
        df["temperature"].between(-90, 60)
        & df["humidity"].between(0, 100)
        & df["wind_speed"].between(0, 300)
    ].copy()

    print("\nCleaned Weather Data:")
    print(df)

    # 4. LOAD: Save cleaned data to MySQL
    cursor = connection.cursor()

    if not df.empty:
        insert_query = """
            INSERT INTO weather_cleaned
            (recorded_at, temperature, humidity, wind_speed)
            VALUES (%s, %s, %s, %s)
        """

        values = [
            (
                row.recorded_at,
                row.temperature,
                row.humidity,
                row.wind_speed
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(insert_query, values)
        connection.commit()

        print("\nCleaned data saved to MySQL!")

    else:
        print("\nNo valid data available.")

    # 5. EXPORT: Save cleaned data as Parquet
    output_dir = Path("data/cleaned")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not df.empty:
        df["recorded_at"] = pd.to_datetime(df["recorded_at"])

        for date, daily_df in df.groupby(
            df["recorded_at"].dt.strftime("%Y-%m-%d")
        ):
            output_file = output_dir / f"weather_{date}.parquet"

            daily_df.to_parquet(output_file, index=False)

            print("Parquet file saved:", output_file)

    print("\nData cleaning and export completed!")

except mysql.connector.Error as error:
    print("MYSQL ERROR:", error)
    if connection is not None and connection.is_connected():
        connection.rollback()

except Exception as error:
    print("ERROR:", error)
    if connection is not None and connection.is_connected():
        connection.rollback()

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")