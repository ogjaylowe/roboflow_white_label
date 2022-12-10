import streamlit as st
import requests

def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

def main():
    workspace = None
    models = []
    dropdown = []

    st.set_page_config(page_title="Roboflow REST API White Label Example", page_icon="🤖")
    st.title("Roboflow REST API White Label Example")
    session = requests.Session()
    with st.form("auth"):
        api_key = st.text_input('API Key', 'YOUR_API_KEY_HERE')

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.write("Workspace Details")
            
            with st.spinner(text="Accessing workspace..."):
                data = fetch(session, f"https://api.roboflow.com/?api_key={api_key}")
            
            if "workspace" in data:
                # st.image(data['download_url'], caption=f"Author: {data['author']}")
                st.success('Workspace found!', icon="✅")
                st.write(data)
                workspace = data["workspace"]
            else:
                st.error("Error - double check API key")
        
        if workspace:
            st.write("Projects")
            with st.spinner(text="Parsing for model endpoints..."):
                data = fetch(session, f"https://api.roboflow.com/{workspace}?api_key={api_key}")
                
                if "workspace" in data and "projects" in data["workspace"]:
                    for project in data["workspace"]["projects"]:
                        id = project["id"].split("/")[1]

                        data2 = fetch(session, f"https://api.roboflow.com/{workspace}/{id}?api_key={api_key}")
                        if data2["versions"]:
                            for version in data2["versions"]:
                                if "model" in version:
                                    models.append(version["model"])

                    st.success('All projects parsed!', icon="✅")

                    for model in models:
                        id = model["id"]
                        map_score = model["map"]
                        dropdown.append(f"{id} - mAP = {map_score}%")

                    option = st.selectbox(
                        'Models available for inference',
                        dropdown)

                else:
                    st.error("Error - No projects found, double check you've created a project in your workspace")


if __name__ == '__main__':
    main()