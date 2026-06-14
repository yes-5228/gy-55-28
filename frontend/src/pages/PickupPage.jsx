import { AlertTriangle, DoorOpen } from "lucide-react";
import React, { useState } from "react";

import { parcelsApi } from "../api/modules";
import MessageBox from "../components/MessageBox";
import PageHeader from "../components/PageHeader";

export default function PickupPage() {
  const [pickupCode, setPickupCode] = useState("");
  const [operator, setOperator] = useState("管理员");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const [showException, setShowException] = useState(false);
  const [exceptionForm, setExceptionForm] = useState({
    exception_type: "wrong_code",
    parcel_tracking_no: "",
    description: "",
  });
  const [exceptionResult, setExceptionResult] = useState("");
  const [exceptionError, setExceptionError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    setResult("");
    setError("");
    try {
      const data = await parcelsApi.open(pickupCode, operator);
      setResult(`${data.message} 运单号 ${data.parcel.tracking_no} 已标记取件。`);
      setPickupCode("");
    } catch (err) {
      setError(err.message);
    }
  };

  const updateException = (event) => {
    setExceptionForm({ ...exceptionForm, [event.target.name]: event.target.value });
  };

  const reportException = async (event) => {
    event.preventDefault();
    setExceptionResult("");
    setExceptionError("");
    try {
      await parcelsApi.reportException({
        ...exceptionForm,
        pickup_code: pickupCode,
        operator,
      });
      setExceptionResult("异常已记录。");
      setExceptionForm({
        exception_type: "wrong_code",
        parcel_tracking_no: "",
        description: "",
      });
    } catch (err) {
      setExceptionError(err.message);
    }
  };

  return (
    <>
      <PageHeader title="取件码开箱" description="输入用户取件码，系统校验后打开对应柜格并更新快件状态。" />
      <section className="pickup-panel">
        <form className="panel code-form" onSubmit={submit}>
          <label>
            操作员
            <input value={operator} onChange={(event) => setOperator(event.target.value)} required />
          </label>
          <label>
            取件码
            <input value={pickupCode} onChange={(event) => setPickupCode(event.target.value)} maxLength={12} required />
          </label>
          <div style={{ display: "flex", gap: 8 }}>
            <button type="submit">
              <DoorOpen size={18} />开箱取件
            </button>
            <button type="button" className="ghost" onClick={() => setShowException(!showException)}>
              <AlertTriangle size={16} />
              {showException ? "收起异常" : "上报异常"}
            </button>
          </div>
          <MessageBox type="success">{result}</MessageBox>
          <MessageBox type="error">{error}</MessageBox>
        </form>
        {showException ? (
          <form className="panel form-panel" style={{ marginTop: 16 }} onSubmit={reportException}>
            <h2>取件异常上报</h2>
            <label>
              异常类型
              <select name="exception_type" value={exceptionForm.exception_type} onChange={updateException}>
                <option value="wrong_code">取件码错误</option>
                <option value="not_found">快件不存在</option>
                <option value="damaged">快件破损</option>
                <option value="other">其他异常</option>
              </select>
            </label>
            <label>
              运单号
              <input
                name="parcel_tracking_no"
                value={exceptionForm.parcel_tracking_no}
                onChange={updateException}
              />
            </label>
            <label>
              描述
              <input name="description" value={exceptionForm.description} onChange={updateException} />
            </label>
            <button type="submit">
              <AlertTriangle size={16} />确认上报
            </button>
            <MessageBox type="success">{exceptionResult}</MessageBox>
            <MessageBox type="error">{exceptionError}</MessageBox>
          </form>
        ) : null}
      </section>
    </>
  );
}
