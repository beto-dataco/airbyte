/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.destination.snowflake;

import com.google.common.collect.ImmutableList;
import java.util.List;

/**
 * See https://docs.snowflake.com/en/sql-reference/reserved-keywords.html Copied from
 * https://github.com/airbytehq/airbyte/blob/f226503bd1d4cd9c7412b04d47de584523988443/airbyte-integrations/bases/base-normalization/normalization/transform_catalog/reserved_keywords.py
 */
public class SnowflakeReservedKeywords {

  public static final List<String> RESERVED_KEYWORDS = ImmutableList.of(
      "ALL",
      "ALTER",
      "AND",
      "ANY",
      "AS",
      "BETWEEN",
      "BY",
      "CASE",
      "CAST",
      "CHECK",
      "COLUMN",
      "CONNECT",
      "CONNECTION",
      "CONSTRAINT",
      "CREATE",
      "CROSS",
      "CURRENT",
      "CURRENT_DATE",
      "CURRENT_TIME",
      "CURRENT_TIMESTAMP",
      "CURRENT_USER",
      "DATABASE",
      "DEFAULT",
      "DELETE",
      "DISTINCT",
      "DROP",
      "ELSE",
      "EXISTS",
      "FALSE",
      "FOLLOWING",
      "FOR",
      "FROM",
      "FULL",
      "GRANT",
      "GROUP",
      "GSCLUSTER",
      "HAVING",
      "ILIKE",
      "IN",
      "INCREMENT",
      "INNER",
      "INSERT",
      "INTERSECT",
      "INTO",
      "IS",
      "ISSUE",
      "JOIN",
      "LATERAL",
      "LEFT",
      "LIKE",
      "LOCALTIME",
      "LOCALTIMESTAMP",
      "MINUS",
      "NATURAL",
      "NOT",
      "NULL",
      "OF",
      "ON",
      "OR",
      "ORDER",
      "ORGANIZATION",
      "QUALIFY",
      "REGEXP",
      "REVOKE",
      "RIGHT",
      "RLIKE",
      "ROW",
      "ROWS",
      "SAMPLE",
      "SCHEMA",
      "SELECT",
      "SET",
      "SOME",
      "START",
      "TABLE",
      "TABLESAMPLE",
      "THEN",
      "TO",
      "TRIGGER",
      "TRUE",
      "TRY_CAST",
      "UNION",
      "UNIQUE",
      "UPDATE",
      "USING",
      "VALUES",
      "VIEW",
      "WHEN",
      "WHENEVER",
      "WHERE",
      "WITH");

  public static final List<String> RESERVED_COLUMN_NAMES = ImmutableList.of(
      "CURRENT_DATE",
      "CURRENT_TIME",
      "CURRENT_TIMESTAMP",
      "CURRENT_USER",
      "LOCALTIME",
      "LOCALTIMESTAMP");

}
