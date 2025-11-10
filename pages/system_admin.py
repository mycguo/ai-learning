import streamlit as st
from app import download_faiss_from_s3, download_s3_bucket   
from pages.app_admin import upload_vector_store_to_s3
from utils.auth import require_login, show_user_info


bucket_name = st.secrets["BUCKET_NAME"]


def main():
    # Check authentication
    if not require_login("System Admin"):
        return
    
    # Show user info in sidebar
    show_user_info()
    
    st.header(f"Welcome, {st.user.name if hasattr(st, 'user') and st.user.is_logged_in else 'Admin'}!")
    st.title("Knowledge Assistant System Admin")
    st.header("System Admin Only: Danger Zone")
    
    if st.button("Upload Vector Store to S3"):
        with st.spinner("Uploading to S3..."):
            upload_vector_store_to_s3()
            st.success("Uploaded to S3!")

    if st.button("Download Vector Store from S3"):
        with st.spinner("Downloading from S3..."):
            download_s3_bucket(bucket_name, "faiss_download")
            st.success("Downloaded file from S3!")

    if st.button("Download Vector Store from S3 and overwrite the local index"):
        with st.spinner("Downloading from S3..."):
            download_s3_bucket(bucket_name, "faiss_index")
            st.success("Downloaded file from S3!")

    st.markdown("---")
    if st.button("🚪 Log out", use_container_width=True):
        if hasattr(st, 'logout'):
            st.logout()
        st.rerun()

if __name__ == "__main__":
    main()