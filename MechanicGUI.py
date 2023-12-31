import streamlit as st
import psycopg2
import pandas as pd


def MechanicMain():
    user_id = st.session_state["user_id"]

    db_params = {
        "host": "localhost",
        "database": "final_project",
        "user": "postgres",
        "password": "Toanposgre"
    }

    try:
        connection = psycopg2.connect(**db_params)
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. {e}")
        st.stop()

    st.title("Mechanic View")

    # Fetch and display data
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT carunchecked.ucid, carunchecked.description, carunchecked.model, carunchecked.year, carunchecked.status FROM brokencar JOIN carunchecked on brokencar.UCID = carunchecked.UCID;")
            data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        st.stop()

    # the broken car table
        # Creating a dataframe from the fetched data
    df = pd.DataFrame(data, columns=colnames)

    df['carPart'] = ''
    df['isFixable'] = False

    edited_df = st.data_editor(df, num_rows="dynamic")

    submitted = st.button("Submit", type="secondary")
    
    if submitted:
        try:
            with connection.cursor() as cursor:
                for index, row in edited_df.iterrows():
                    
                    if row['isFixable']:
                        # Placeholder for action when 'isCarGood' is True
                        st.write(f"ID {row['ucid']} is True. Do something here.")
                        
                        # Write SQL query to add to greatcar table
                        cursor.execute(f"""
                            INSERT INTO greatcar (ucid)
                            VALUES ( {int(row['ucid'])} );
                        """)

                        # remove from broken car table
                        cursor.execute(
                            """
                            DELETE FROM brokencar 
                            WHERE ucid = %s;
                            """,
                            (int(row['ucid']),)
                        )

                    else:
                        # Placeholder for action when 'isCarGood' is False
                        st.write(f"ID {row['ucid']} is False. Do something else here.")

                        # query to add to BrokenCar
                        st.write('car part', row["carPart"])
                        cursor.execute(f"""
                            INSERT INTO CarParts (cid, mechanicid, partname)
                            VALUES ( {int(row['ucid'])}, {int(user_id)}, 'To be updated...' );
                        """)

                        cursor.execute(
                            """
                            DELETE FROM brokencar 
                            WHERE ucid = %s;
                            """,
                            (int(row['ucid']),)
                        )

                # Updating all 'Uncheck' values to False
                # cursor.execute("UPDATE carunchecked SET uncheck = False WHERE uncheck = True;")
                connection.commit()

        except Exception as e:
            st.error(f"Error: Unable to update the database. {e}")

        finally:
            # Refetching the data after the update
            print()
            st.experimental_rerun()
            # try:
            #     with connection.cursor() as cursor:
            #         cursor.execute("SELECT * FROM carunchecked WHERE uncheck = True;")
            #         data = cursor.fetchall()
            #         colnames = [desc[0] for desc in cursor.description]
            #         df = pd.DataFrame(data, columns=colnames)
            #         df_display = df.drop(columns=['uncheck'])
            #         df_display['isCarGood'] = False
            #         st.table(df_display)
            # except Exception as e:
            #     st.error(f"Error: Unable to fetch the updated data. {e}")



