-- augur_data.explorer_cntrb_per_file source

CREATE MATERIALIZED VIEW augur_data.explorer_cntrb_per_file
TABLESPACE pg_default
AS SELECT pr.repo_id,
    prf.pr_file_path AS file_path,
    string_agg(DISTINCT pr.pr_augur_contributor_id::character varying(15)::text, ','::text) AS cntrb_ids,
    string_agg(DISTINCT prr.cntrb_id::character varying(15)::text, ','::text) AS reviewer_ids
   FROM augur_data.pull_requests pr
     JOIN augur_data.pull_request_files prf ON pr.pull_request_id = prf.pull_request_id
     LEFT JOIN augur_data.pull_request_reviews prr ON pr.pull_request_id = prr.pull_request_id
  GROUP BY prf.pr_file_path, pr.repo_id
WITH DATA;

-- View indexes:
CREATE INDEX idx_explorer_cntrb_per_file_repo_id ON augur_data.explorer_cntrb_per_file USING btree (repo_id);