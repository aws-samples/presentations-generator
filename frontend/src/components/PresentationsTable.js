import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Box,
  Typography,
  TableSortLabel,
} from "@mui/material";
import { useState } from "react";
import RefreshIcon from "@mui/icons-material/Refresh";
import ImageIcon from "@mui/icons-material/Image";
import api from "../services/api";

const columns = [
  { id: "timestamp", label: "Data/Hora", minWidth: 170 },
  { id: "session_id", label: "Sessão", minWidth: 300 },
  { id: "user_request", label: "Requisição", minWidth: 200 },
  { id: "output_filename", label: "Apresentação", minWidth: 100 },
];

function PresentationsTable({ presentations, onRefresh }) {
  // const [reportModal, setReportModal] = useState(false);
  const [sortConfig, setSortConfig] = useState({
    key: "timestamp",
    direction: "asc",
  });

  const handleOpenImage = async (filename) => {
    try {
      const response = await api.get(`/download?filename=${encodeURIComponent(filename)}`);
      const presignedUrl = response.data.presigned_url;
      return presignedUrl;
    } catch (error) {
      console.error(error);
      return null;
    }
  };

  const handleSort = (columnId) => {
    const isAsc = sortConfig.key === columnId && sortConfig.direction === "asc";
    setSortConfig({ key: columnId, direction: isAsc ? "desc" : "asc" });
  };

  const sortedPresentations = [...presentations].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) {
      return sortConfig.direction === "asc" ? -1 : 1;
    }
    if (a[sortConfig.key] > b[sortConfig.key]) {
      return sortConfig.direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  return (
    <Paper sx={{ width: "100%", overflow: "hidden" }}>
      <Box
        sx={{
          display: "flex",
          flexDirection: "row-reverse",
        }}
      >
        <Button onClick={onRefresh}>
          <RefreshIcon />
        </Button>
      </Box>
      <TableContainer sx={{ maxHeight: 2000 }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                >
                  <TableSortLabel
                    active={sortConfig.key === column.id}
                    direction={
                      sortConfig.key === column.id
                        ? sortConfig.direction
                        : "asc"
                    }
                    onClick={() => handleSort(column.id)}
                  >
                    {column.label}
                  </TableSortLabel>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedPresentations.map((row) => (
              <TableRow key={row.id}>
                {columns.map((column) => {
                  const value = row[column.id];
                  if (column.id === "output_filename") {
                    return (
                      <TableCell key={column.id} align={column.align}>
                        {value !== "" ? (
                          <Button
                            onClick={async () => {
                              try {
                                const url = await handleOpenImage(row.output_filename);
                                window.open(url, "_blank");
                              } catch (error) {
                                console.error("Error opening image:", error);
                                // Handle error (e.g., show a message to the user)
                              }
                            }}
                          >
                            <ImageIcon />
                          </Button>
                        ) : (
                          <Typography>aguardando</Typography>
                        )}
                      </TableCell>
                    );

                  } else {
                    return (
                      <TableCell key={column.id} align={column.align}>
                        <Typography>
                          {value !== "" ? value : "aguardando"}
                        </Typography>
                      </TableCell>
                    );
                  }
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default PresentationsTable;
