-- augur_data.explorer_cntrb_per_file source

CREATE MATERIALIZED VIEW IF NOT EXISTS augur_data.explorer_cntrb_per_file AS
SELECT
    pr.repo_id as repo_id,
    prf.pr_file_path as file_path,
    string_agg(DISTINCT CAST(pr.pr_augur_contributor_id AS varchar(15)), ',') AS cntrb_ids,
    string_agg(DISTINCT CAST(prr.cntrb_id AS varchar(15)), ',') AS reviewer_ids
FROM
    augur_data.pull_requests pr
INNER JOIN
    augur_data.pull_request_files prf
ON
    pr.pull_request_id = prf.pull_request_id
LEFT OUTER JOIN
    augur_data.pull_request_reviews prr
ON
    pr.pull_request_id = prr.pull_request_id
GROUP BY prf.pr_file_path, pr.repo_id
WITH NO DATA;

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_explorer_cntrb_per_file_repo_id ON augur_data.explorer_cntrb_per_file USING btree (repo_id);