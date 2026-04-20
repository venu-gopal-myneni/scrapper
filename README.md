Build
--------------------
1) uv build


Setup on remote server
-------------------------
1) login to remote server
2) Install uv
 curl -LsSf https://astral.sh/uv/install.sh | sh
3) Install python
uv python install 3.12
5) Install duckdb
curl https://install.duckdb.org | sh
6) open duckdb and install httpfs, aws, ducklake extensions

4) Transfer wheel file
scp -i key.pem file.txt ec2-user@EC2_PUBLIC_IP:/home/ec2-user/
5) Transfer env file and update
6) Create virtual env and install wheel file
7) create tables in ducklake

OR
Start the EC2 server
Add HOST name in secrets of Github
Do a tag push -> autobuild and deploy through Github actions


