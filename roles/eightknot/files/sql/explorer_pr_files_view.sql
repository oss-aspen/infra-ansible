-- Create explorer_pr_files materialized view

CREATE MATERIALIZED VIEW IF NOT EXISTS augur_data.explorer_pr_files AS
SELECT
    prf.pr_file_path as file_path,
    pr.pull_request_id AS pull_request_id,
    pr.repo_id as repo_id
FROM
    augur_data.pull_requests pr
INNER JOIN
    augur_data.pull_request_files prf
ON
    pr.pull_request_id = prf.pull_request_id
WITH NO DATA;

-- Create index for performance
CREATE INDEX idx_explorer_pr_files_repo_id ON augur_data.explorer_pr_files(repo_id);