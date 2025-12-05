-- augur_data.explorer_pr_files source

CREATE MATERIALIZED VIEW augur_data.explorer_pr_files
TABLESPACE pg_default
AS SELECT prf.pr_file_path AS file_path,
    pr.pull_request_id,
    pr.repo_id
   FROM augur_data.pull_requests pr
     JOIN augur_data.pull_request_files prf ON pr.pull_request_id = prf.pull_request_id
WITH NO DATA;

-- View indexes:
CREATE INDEX idx_explorer_pr_files_repo_id ON augur_data.explorer_pr_files USING btree (repo_id);