from aws_cdk import App, Environment
from cdk_py.cdk_py_stack import CdkEc2Stack

# Definir la cuenta y la región de AWS manualmente
env = Environment(account="946144080964", region="us-east-1")

app = App()
CdkEc2Stack(app, "cdk-ec2-stack", env=env)

app.synth()

