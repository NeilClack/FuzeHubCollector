CREATE TABLE IF NOT EXISTS models 
(
	model_id INT PRIMARY KEY,
	name VARCHAR(80) NOT NULL,
	likes INT NOT NULL,
	slug text,
	uri text,
	image_uri text[],
	last_update TIMESTAMP NOT NULL,
	date_added TIMESTAMPT NOT NULL DEFAULT (now() in time zone 'utc')
);