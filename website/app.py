from flask import Flask, render_template, request  # type: ignore
import pickle
import numpy as np
 

# Set up the application
app = Flask(__name__)

def prediction(lst):
    filename ='model/predictor.pickle'
    with open(filename,'rb')as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value
    
# Create webpages
@app.route("/", methods=["POST", "GET"])
def index():
    pred = 0
    if request.method == "POST":
        try:
            # Get form data
            Ram = request.form.get("Ram")
            Weight = request.form.get("Weight")
            Touchscreen = request.form.get("Touchscreen")
            Ips = request.form.get("Ips")
            Company = request.form.get("Company")
            TypeName = request.form.get("TypeName")
            OpSys = request.form.get("OpSys")
            cpu_name = request.form.get("cpu_name")
            gpu_name = request.form.get("gpu_name")

            # Prepare feature list
            feature_list = []
            feature_list.append(int(Ram))
            feature_list.append(float(Weight))
            feature_list.append(1 if Touchscreen == "True" else 0)
            feature_list.append(1 if Ips == "True" else 0)

            # Categorical lists
            company_list = ["acer", "apple", "asus", "dell", "hp", "lenovo", "msi", "other", "toshiba"]
            typename_list = ["2in1convertible", "gaming", "netbook", "notebook", "ultrabook", "workstation"]
            opsys_list = ["linux", "mac", "other", "windows"]
            cpu_list = ["amd", "intelcorei3", "intelcorei5", "intelcorei7", "other"]
            gpu_list = ["amd", "intel", "nvidia"]

            # Convert dropdown input to lowercase for matching
            Company = Company.lower()
            TypeName = TypeName.replace(" ", "").lower()
            OpSys = OpSys.lower()
            cpu_name = cpu_name.replace(" ", "").lower()
            gpu_name = gpu_name.lower()

            # Categorical encoding
            def traverse_list(lst, value):
                for item in lst:
                    feature_list.append(1 if item == value else 0)

            traverse_list(company_list, Company)
            traverse_list(typename_list, TypeName)
            traverse_list(opsys_list, OpSys)
            traverse_list(cpu_list, cpu_name)
            traverse_list(gpu_list, gpu_name)

            pred = prediction (feature_list)*313
            pred=np.round(pred[0])
            

        except Exception as e:
            print(f"Error occurred: {e}")

    return render_template("index.html" , pred=pred)


if __name__ == "__main__":
    app.run(debug=True)
