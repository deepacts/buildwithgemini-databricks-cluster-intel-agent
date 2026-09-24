# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Seed script for populating Databricks cluster data into Firestore."""

from google.cloud import firestore

# Hardcoded project ID as explicitly required for Firestore client
PROJECT_ID = "qwiklabs-gcp-02-7222a271d6bd"
COLLECTION_NAME = "databricks_clusters"


def seed_data():
    db = firestore.Client(project=PROJECT_ID)
    collection = db.collection(COLLECTION_NAME)

    sample_clusters = [
        {
            "cluster_id": "cluster-01",
            "cluster_name": "analytics-etl-prod",
            "node_type": "i3.xlarge",
            "num_workers": 8,
            "state": "RUNNING",
            "auto_termination_minutes": 120,
            "monthly_cost_usd": 1450.00,
            "optimization_recommendation": "Downsize to i3.large or lower auto-termination to 30 mins to save $600/month",
        },
        {
            "cluster_id": "cluster-02",
            "cluster_name": "data-science-dev",
            "node_type": "m5d.2xlarge",
            "num_workers": 4,
            "state": "IDLE",
            "auto_termination_minutes": 180,
            "monthly_cost_usd": 980.00,
            "optimization_recommendation": "Cluster idle for >4 hours; enable auto-scaling (1-4 nodes) to save $450/month",
        },
        {
            "cluster_id": "cluster-03",
            "cluster_name": "sql-warehouse-bi",
            "node_type": "c5.2xlarge",
            "num_workers": 12,
            "state": "RUNNING",
            "auto_termination_minutes": 60,
            "monthly_cost_usd": 2100.00,
            "optimization_recommendation": "Optimal sizing for peak BI queries; monitor off-peak weekend usage",
        },
    ]

    for cluster in sample_clusters:
        doc_ref = collection.document(cluster["cluster_id"])
        doc_ref.set(cluster)
        print(f"Seeded {cluster['cluster_id']}: {cluster['cluster_name']}")

    print(f"Successfully seeded {len(sample_clusters)} clusters into Firestore collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    seed_data()
