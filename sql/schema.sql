-- スキーマ定義
CREATE TABLE IF NOT EXISTS kind_question (
    kind_id INT PRIMARY KEY,
    kind_question VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS question (
    q_id INT AUTO_INCREMENT PRIMARY KEY,
    kind_id INT,
    question VARCHAR(200) NOT NULL,
    FOREIGN KEY (kind_id) REFERENCES kind_question(kind_id)
);

CREATE TABLE IF NOT EXISTS answer (
    ans_id INT AUTO_INCREMENT PRIMARY KEY,
    q_id INT,
    kind_id INT,
    answer VARCHAR(1000) NOT NULL,
    FOREIGN KEY (q_id) REFERENCES question(q_id),
    FOREIGN KEY (kind_id) REFERENCES kind_question(kind_id)
);

