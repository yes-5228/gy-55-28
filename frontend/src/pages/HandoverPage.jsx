import { AlertTriangle, ArrowLeftRight, PackagePlus, RefreshCw, RotateCcw } from "lucide-react";
import React, { useEffect, useState } from "react";

import { handoversApi } from "../api/modules";
import DataTable from "../components/DataTable";
import MessageBox from "../components/MessageBox";
import MetricCard from "../components/MetricCard";
import PageHeader from "../components/PageHeader";

function formatDateTime(dt) {
  if (!dt) return "-";
  return new Date(dt).toLocaleString("zh-CN", { hour12: false });
}

const defaultOperator = "管理员";

export default function HandoverPage() {
  const [shifts, setShifts] = useState([]);
  const [exceptions, setExceptions] = useState([]);
  const [previewStats, setPreviewStats] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const now = new Date();
  const todayStr = now.toISOString().slice(0, 10);
  const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 8, 0, 0);
  const endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 20, 0, 0);

  const [form, setForm] = useState({
    courier_name: defaultOperator,
    shift_start: startOfDay.toISOString().slice(0, 16),
    shift_end: endOfDay.toISOString().slice(0, 16),
    remark: "",
    handed_by: defaultOperator,
    received_by: "",
  });

  const load = async () => {
    const [shiftData, exceptionData] = await Promise.all([
      handoversApi.listShifts(),
      handoversApi.listExceptions(),
    ]);
    setShifts(shiftData);
    setExceptions(exceptionData);
  };

  useEffect(() => {
    load();
  }, []);

  const updateField = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const preview = async () => {
    setMessage("");
    setError("");
    try {
      const stats = await handoversApi.getStats({
        courier_name: form.courier_name,
        shift_start: new Date(form.shift_start).toISOString(),
        shift_end: new Date(form.shift_end).toISOString(),
      });
      setPreviewStats(stats);
    } catch (err) {
      setError(err.message);
    }
  };

  const submit = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");
    try {
      await handoversApi.createShift({
        courier_name: form.courier_name,
        shift_start: new Date(form.shift_start).toISOString(),
        shift_end: new Date(form.shift_end).toISOString(),
        remark: form.remark,
        handed_by: form.handed_by,
        received_by: form.received_by,
      });
      setMessage("交接班记录已创建。");
      setPreviewStats(null);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <PageHeader
        title="快递员交接班统计"
        description="记录当班入库数量、取件异常和退件处理数量，完成交接班确认。"
      />
      {previewStats ? (
        <div className="metric-grid compact" style={{ marginBottom: 20 }}>
          <MetricCard title="当班入库" value={previewStats.inbound_count} hint="件" icon={PackagePlus} />
          <MetricCard
            title="取件异常"
            value={previewStats.pickup_exception_count}
            hint="次"
            icon={AlertTriangle}
          />
          <MetricCard
            title="退件处理"
            value={previewStats.return_processed_count}
            hint="件"
            icon={RotateCcw}
          />
          <MetricCard
            title="合计"
            value={previewStats.inbound_count + previewStats.pickup_exception_count + previewStats.return_processed_count}
            hint="项操作"
            icon={ArrowLeftRight}
          />
        </div>
      ) : null}
      <section className="work-grid">
        <form className="panel form-panel" onSubmit={submit}>
          <h2>交接班登记</h2>
          <label>
            当班快递员
            <input name="courier_name" value={form.courier_name} onChange={updateField} required />
          </label>
          <label>
            交班开始时间
            <input
              name="shift_start"
              type="datetime-local"
              value={form.shift_start}
              onChange={updateField}
              required
            />
          </label>
          <label>
            交班结束时间
            <input
              name="shift_end"
              type="datetime-local"
              value={form.shift_end}
              onChange={updateField}
              required
            />
          </label>
          <label>
            交班人
            <input name="handed_by" value={form.handed_by} onChange={updateField} required />
          </label>
          <label>
            接班人
            <input name="received_by" value={form.received_by} onChange={updateField} />
          </label>
          <label>
            备注
            <input name="remark" value={form.remark} onChange={updateField} />
          </label>
          <div style={{ display: "flex", gap: 8 }}>
            <button type="button" className="ghost" onClick={preview}>
              <RefreshCw size={16} />预览统计
            </button>
            <button type="submit">
              <ArrowLeftRight size={18} />确认交接
            </button>
          </div>
          <MessageBox type="success">{message}</MessageBox>
          <MessageBox type="error">{error}</MessageBox>
        </form>
        <section className="panel">
          <div className="panel-title">
            <h2>交接班记录</h2>
            <button className="ghost" onClick={load}>
              <RefreshCw size={16} />刷新
            </button>
          </div>
          <DataTable
            rows={shifts}
            columns={[
              { key: "courier_name", title: "当班快递员" },
              { key: "shift_start", title: "开始时间", render: (row) => formatDateTime(row.shift_start) },
              { key: "shift_end", title: "结束时间", render: (row) => formatDateTime(row.shift_end) },
              { key: "inbound_count", title: "入库" },
              { key: "pickup_exception_count", title: "取件异常" },
              { key: "return_processed_count", title: "退件处理" },
              { key: "handed_by", title: "交班人" },
              { key: "received_by", title: "接班人" },
            ]}
          />
        </section>
      </section>
      <section className="panel" style={{ marginTop: 18 }}>
        <div className="panel-title">
          <h2>取件异常记录</h2>
        </div>
        <DataTable
          rows={exceptions}
          columns={[
            { key: "exception_type_label", title: "异常类型" },
            { key: "parcel_tracking_no", title: "运单号" },
            { key: "pickup_code", title: "取件码" },
            { key: "operator", title: "操作员" },
            { key: "description", title: "描述" },
            { key: "created_at", title: "时间", render: (row) => formatDateTime(row.created_at) },
          ]}
        />
      </section>
    </>
  );
}
