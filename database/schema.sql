-- Drop tables if they exist
DROP TABLE IF EXISTS Mentor;
DROP TABLE IF EXISTS R;
DROP TABLE IF EXISTS Subscription;
DROP TABLE IF EXISTS Articles;
DROP TABLE IF EXISTS Writer;
DROP TABLE IF EXISTS NewsPaper;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS NewsGroup;

-- Create tables
CREATE TABLE NewsGroup (
    NewsGroupID varchar(6),
    NewsGroupName varchar(20) NOT NULL,
    Country varchar(20) NOT NULL,
    revenue numeric(10,2) DEFAULT 0,
    PRIMARY KEY(NewsGroupID),
    CHECK (Revenue >= 0)
);

CREATE TABLE Users (
    User_ID varchar(6),
    name varchar(20) NOT NULL,
    password varchar(20) NOT NULL,
    Email varchar(50) UNIQUE,
    Total_Articles_Read numeric(4),
    Total_Articles_Rated numeric(4),
    Last_Active_Date date,
    PRIMARY KEY(User_ID),
    CHECK (Total_Articles_Read >= 0),
    CHECK (Total_Articles_Rated >= 0)
);

CREATE TABLE NewsPaper (
    Paper_Name varchar(20),
    Language varchar(20) NOT NULL,
    Editor_in_chief varchar(20) NOT NULL,
    NewsGroupID varchar(6) NOT NULL,
    PRIMARY KEY(Paper_Name),
    FOREIGN KEY(NewsGroupID) REFERENCES NewsGroup(NewsGroupID)
);

CREATE TABLE Writer (
    Writer_ID varchar(6),
    name varchar(20),
    email varchar(50) UNIQUE,
    password varchar(20),
    NewsGroupID varchar(6),
    PRIMARY KEY(Writer_ID),
    FOREIGN KEY(NewsGroupID) REFERENCES NewsGroup(NewsGroupID)
);

CREATE TABLE Articles (
    Paper_Name varchar(20),
    Title varchar(20),
    Writer_ID varchar(6),
    Published_Date date,
    PRIMARY KEY(Paper_Name, Title),
    FOREIGN KEY(Paper_Name) REFERENCES NewsPaper(Paper_Name),
    FOREIGN KEY(Writer_ID) REFERENCES Writer(Writer_ID)
);

CREATE TABLE Subscription (
    User_ID varchar(6),
    NewsGroupID varchar(6),
    Subscription_Rate numeric(7,2) DEFAULT 0,
    Fee numeric(7,2),
    PRIMARY KEY(User_ID, NewsGroupID),
    FOREIGN KEY(User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY(NewsGroupID) REFERENCES NewsGroup(NewsGroupID),
    CHECK (Subscription_Rate >= 0)
);

CREATE TABLE R (
    User_ID varchar(6),
    Paper_Name varchar(20),
    Title varchar(20),
    rating numeric(2),
    Read_Date date,
    PRIMARY KEY(User_ID, Paper_Name, Title),
    FOREIGN KEY(User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY(Paper_Name, Title) REFERENCES Articles(Paper_Name, Title),
    CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE Mentor (
    Mentor_ID varchar(6) NOT NULL,
    Mentee_ID varchar(6) NOT NULL,
    PRIMARY KEY(Mentor_ID, Mentee_ID),
    FOREIGN KEY(Mentor_ID) REFERENCES Writer(Writer_ID),
    FOREIGN KEY(Mentee_ID) REFERENCES Writer(Writer_ID)
);