-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 25 Lis 2025, 07:29
-- Wersja serwera: 10.4.27-MariaDB
-- Wersja PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Tworzenie bazy jeśli nie istnieje
CREATE DATABASE IF NOT EXISTS `livepoll` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `livepoll`;

--
-- Baza danych: `livepoll`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `answers`
--

CREATE TABLE `answers` (
  `id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `text` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `answers`
--

INSERT INTO `answers` (`id`, `question_id`, `text`) VALUES
(469, 185, 'Niebieski'),
(470, 185, 'Czerwony'),
(471, 185, 'Zielony'),
(472, 186, 'Włoska'),
(473, 186, 'Japońska'),
(474, 186, 'Meksykańska'),
(475, 186, 'Polska'),
(476, 187, 'Piłka nożna'),
(477, 187, 'Siatkówka'),
(478, 187, 'Koszykówka'),
(479, 188, 'Windows'),
(480, 188, 'Linux'),
(481, 188, 'MacOS'),
(482, 189, 'Kawa'),
(483, 189, 'Herbata'),
(484, 189, 'Nic z tego'),
(485, 190, 'Autobus'),
(486, 190, 'Tramwaj'),
(487, 190, 'Metro'),
(488, 191, 'RPG'),
(489, 191, 'FPS'),
(490, 191, 'Strategie'),
(491, 191, 'Wyścigi'),
(492, 192, 'Komedia'),
(493, 192, 'Sci-Fi'),
(494, 192, 'Horror'),
(495, 193, 'Rzadko'),
(496, 193, 'Kilka razy w roku'),
(497, 193, 'Często'),
(498, 194, 'Fantastyka'),
(499, 194, 'Kryminał'),
(500, 194, 'Popularnonaukowe'),
(501, 194, 'Obyczajowe'),
(502, 195, 'Rock'),
(503, 195, 'Pop'),
(504, 195, 'Jazz'),
(505, 195, 'Hip-Hop'),
(506, 196, 'Czytanie'),
(507, 196, 'Sport'),
(508, 196, 'Gotowanie'),
(509, 196, 'Podróże'),
(510, 197, 'Nike'),
(511, 197, 'Adidas'),
(512, 197, 'Puma'),
(513, 197, 'Reebok'),
(514, 198, 'Pies'),
(515, 198, 'Kot'),
(516, 198, 'Chomik'),
(517, 198, 'Papuga'),
(518, 199, 'Platon'),
(519, 199, 'Arystoteles'),
(520, 199, 'Kant'),
(521, 200, 'IT'),
(522, 200, 'Marketing'),
(523, 200, 'Finanse'),
(524, 200, 'Edukacja'),
(525, 201, 'Komedia'),
(526, 201, 'Thriller'),
(527, 201, 'Dramat'),
(528, 201, 'Sci-Fi'),
(529, 202, 'Toyota'),
(530, 202, 'BMW'),
(531, 202, 'Audi'),
(532, 203, 'Szachy'),
(533, 203, 'Monopoly'),
(534, 203, 'Carcassonne'),
(535, 203, 'Scrabble'),
(536, 204, 'Pizza'),
(537, 204, 'Sushi'),
(538, 204, 'Tacos'),
(539, 204, 'Pierogi');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `polls`
--

CREATE TABLE `polls` (
  `id` char(8) NOT NULL,
  `title` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `visibility` enum('public','restricted') NOT NULL DEFAULT 'public'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `polls`
--

INSERT INTO `polls` (`id`, `title`, `user_id`, `created_at`, `visibility`) VALUES
('a1b2c3d4', 'Ulubiony kolor', NULL, '2025-11-25 06:27:03', 'public'),
('b1c2d3e4', 'Filozofia', NULL, '2025-11-25 06:27:03', 'public'),
('c3v4b5n6', 'Podróże', NULL, '2025-11-25 06:27:03', 'public'),
('e5f6g7h8', 'Preferencje kulinarne', NULL, '2025-11-25 06:27:03', 'public'),
('f5g6h7i8', 'Praca', NULL, '2025-11-25 06:27:03', 'public'),
('j1k2l3m4', 'Seriale', NULL, '2025-11-25 06:27:03', 'public'),
('l1k2j3h4', 'Gry komputerowe', NULL, '2025-11-25 06:27:03', 'public'),
('m1n2b3v4', 'Książki', NULL, '2025-11-25 06:27:03', 'public'),
('n1o2p3q4', 'Muzyka', NULL, '2025-11-25 06:27:03', 'public'),
('n5o6p7q8', 'Motoryzacja', NULL, '2025-11-25 06:27:03', 'restricted'),
('p0o9i8u7', 'Transport miejski', NULL, '2025-11-25 06:27:03', 'restricted'),
('q9w8e7r6', 'Technologia', NULL, '2025-11-25 06:27:03', 'public'),
('r1s2t3u4', 'Gry planszowe', NULL, '2025-11-25 06:27:03', 'public'),
('r5s6t7u8', 'Hobby', NULL, '2025-11-25 06:27:03', 'public'),
('s5t6u7v8', 'Podróże kulinarne', NULL, '2025-11-25 06:27:03', 'public'),
('t5y4u3i2', 'Kawa czy herbata?', NULL, '2025-11-25 06:27:03', 'public'),
('v6b7n8m9', 'Filmy', NULL, '2025-11-25 06:27:03', 'public'),
('w1x2y3z4', 'Moda', NULL, '2025-11-25 06:27:03', 'public'),
('x1y2z3w4', 'Sporty', NULL, '2025-11-25 06:27:03', 'restricted'),
('y5z6a7b8', 'Zwierzęta', NULL, '2025-11-25 06:27:03', 'public');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `poll_id` char(8) NOT NULL,
  `text` varchar(255) NOT NULL,
  `type` enum('single','multi') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `questions`
--

INSERT INTO `questions` (`id`, `poll_id`, `text`, `type`) VALUES
(185, 'a1b2c3d4', 'Jaki jest Twój ulubiony kolor?', 'single'),
(186, 'e5f6g7h8', 'Jakie kuchnie lubisz najbardziej?', 'multi'),
(187, 'x1y2z3w4', 'Jakie sporty oglądasz?', 'multi'),
(188, 'q9w8e7r6', 'Jaki system operacyjny preferujesz?', 'single'),
(189, 't5y4u3i2', 'Co pijesz częściej?', 'single'),
(190, 'p0o9i8u7', 'Z czego korzystasz najczęściej?', 'single'),
(191, 'l1k2j3h4', 'W jakie gatunki grasz najczęściej?', 'multi'),
(192, 'v6b7n8m9', 'Jaki gatunek filmowy preferujesz?', 'single'),
(193, 'c3v4b5n6', 'Jak często podróżujesz?', 'single'),
(194, 'm1n2b3v4', 'Jakie gatunki książek czytasz?', 'multi'),
(195, 'n1o2p3q4', 'Jakiego rodzaju muzyki słuchasz?', 'multi'),
(196, 'r5s6t7u8', 'Jakie masz hobby?', 'multi'),
(197, 'w1x2y3z4', 'Jakie marki ubrań preferujesz?', 'multi'),
(198, 'y5z6a7b8', 'Jakie zwierzęta posiadasz?', 'multi'),
(199, 'b1c2d3e4', 'Który filozof najbardziej Cię interesuje?', 'single'),
(200, 'f5g6h7i8', 'Jakie są Twoje preferencje zawodowe?', 'multi'),
(201, 'j1k2l3m4', 'Jakie seriale oglądasz najczęściej?', 'multi'),
(202, 'n5o6p7q8', 'Jakie marki samochodów lubisz?', 'single'),
(203, 'r1s2t3u4', 'Jakie gry planszowe grasz najczęściej?', 'multi'),
(204, 's5t6u7v8', 'Które dania lubisz najbardziej?', 'multi');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `votes`
--

CREATE TABLE `votes` (
  `id` int(11) NOT NULL,
  `poll_id` char(8) NOT NULL,
  `question_id` int(11) NOT NULL,
  `answer_id` int(11) NOT NULL,
  `session_id` varchar(64) NOT NULL,
  `voted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `answers`
--
ALTER TABLE `answers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question_id` (`question_id`);

--
-- Indeksy dla tabeli `polls`
--
ALTER TABLE `polls`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeksy dla tabeli `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `poll_id` (`poll_id`);

--
-- Indeksy dla tabeli `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeksy dla tabeli `votes`
--
ALTER TABLE `votes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_votes_poll` (`poll_id`),
  ADD KEY `idx_votes_question` (`question_id`),
  ADD KEY `idx_votes_answer` (`answer_id`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `answers`
--
ALTER TABLE `answers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=540;

--
-- AUTO_INCREMENT dla tabeli `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=205;

--
-- AUTO_INCREMENT dla tabeli `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `votes`
--
ALTER TABLE `votes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `answers`
--
ALTER TABLE `answers`
  ADD CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE;

--
-- Ograniczenia dla tabeli `polls`
--
ALTER TABLE `polls`
  ADD CONSTRAINT `polls_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Ograniczenia dla tabeli `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`poll_id`) REFERENCES `polls` (`id`) ON DELETE CASCADE;

--
-- Ograniczenia dla tabeli `votes`
--
ALTER TABLE `votes`
  ADD CONSTRAINT `votes_ibfk_1` FOREIGN KEY (`poll_id`) REFERENCES `polls` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `votes_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `votes_ibfk_3` FOREIGN KEY (`answer_id`) REFERENCES `answers` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
