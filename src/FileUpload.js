import React, { Component } from "react";
import Dropzone from "react-dropzone";
import "./styles.css";
import axios from "axios";

class FileUpload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pickerMessage: "Click me or drag a file to upload!",
      uploadedFile: null,
      items: [],
      errorMessage: "",
    };
  }

  handleUpload = (e) => {
    e.preventDefault();
    const baseUrl = process.env.REACT_APP_BASE_URL;
    const formData = new FormData();
    formData.append("file", this.state.uploadedFile);
    axios
      .post(`${baseUrl}api/v1/facts/upload/`, formData, {
        headers: {
          "content-type": "multipart/form-data",
        },
      })
      .then(
        (response) => {
          this.setState({ items: response.data });
          console.log(response);
        },
        (error) => {
          this.setState({ errorMessage: error.message });
          console.log(error);
        }
      );
  };

  onDrop = (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    const filePath = uploadedFile.path;
    const fileSize =
      Math.round((uploadedFile.size / 1000000 + Number.EPSILON) * 10) / 10;
    this.setState({ pickerMessage: `${filePath} (${fileSize} MB)` });
    this.setState({ uploadedFile: uploadedFile });
  };

  render() {
    return (
      <section className="container">
        {this.state.errorMessage && (
          <h3 className="error"> {this.state.errorMessage} </h3>
        )}
        <div className="pickerContainer">
          <Dropzone onDrop={this.onDrop}>
            {({ getRootProps, getInputProps, isDragActive }) => (
              <div className="filePicker" {...getRootProps()}>
                <input {...getInputProps()} />
                <svg
                  className="box__icon"
                  xmlns="http://www.w3.org/2000/svg"
                  width="50"
                  height="43"
                  viewBox="0 0 50 43"
                >
                  <path d="M48.4 26.5c-.9 0-1.7.7-1.7 1.7v11.6h-43.3v-11.6c0-.9-.7-1.7-1.7-1.7s-1.7.7-1.7 1.7v13.2c0 .9.7 1.7 1.7 1.7h46.7c.9 0 1.7-.7 1.7-1.7v-13.2c0-1-.7-1.7-1.7-1.7zm-24.5 6.1c.3.3.8.5 1.2.5.4 0 .9-.2 1.2-.5l10-11.6c.7-.7.7-1.7 0-2.4s-1.7-.7-2.4 0l-7.1 8.3v-25.3c0-.9-.7-1.7-1.7-1.7s-1.7.7-1.7 1.7v25.3l-7.1-8.3c-.7-.7-1.7-.7-2.4 0s-.7 1.7 0 2.4l10 11.6z"></path>
                </svg>
                <div style={{ marginTop: "25px" }}>
                  {isDragActive ? "Drop to Donate!" : this.state.pickerMessage}
                </div>
              </div>
            )}
          </Dropzone>
        </div>
        <button className="buttonStyle" onClick={this.handleUpload}>
          Donate!
        </button>
      </section>
    );
  }
}

export default FileUpload;
