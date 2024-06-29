
import streamlit as st
from io import BytesIO
import pdf_utils
import mcq_generator


def main():
    st.title("MCQ Generator for Exams from PDF")

    uploaded_files = st.file_uploader(
        "Upload PDF file(s)", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            pdf_data = BytesIO(uploaded_file.read())
            text = pdf_utils.extract_text_from_pdf(pdf_data)
            st.markdown(f"### Extracted Text from {uploaded_file.name}:")
            st.text_area(f"{uploaded_file.name} Text", text, height=400)

            num_questions = st.number_input(
                "Number of MCQs to generate:",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
            )

            num_distractors = st.number_input(
                "Number of distractors per question:",
                min_value=2,
                max_value=5,
                value=3,
                step=1,
            )

            if st.button("Generate MCQs"):
                mcqs = mcq_generator.generate_mcqs(text, num_questions, num_distractors)

                st.markdown("### Generated MCQs:")
                for i, mcq in enumerate(mcqs):
                    st.markdown(f"**Question {i+1}:** {mcq[0]}")
                    options_text = "\n".join(
                        [f"{chr(65 + j)}. {option}" for j, option in enumerate(mcq[1])]
                    )
                    st.markdown(f"Options:\n{options_text}")

            
                    with st.expander(f"Show Correct Answer for Question {i+1}"):
                        st.markdown(f"Correct Answer: {mcq[2]}")


if __name__ == "__main__":
    main()
