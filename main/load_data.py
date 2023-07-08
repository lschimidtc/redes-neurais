import numpy as np
import os


def load_var(path, ip_len=3, op_len=20, out_put_one=False):
    ip_data_ls = []
    op_data_ls = []
    ip_data_ls1 = []
    sst = np.load(path + "/sst.npy")
    ssh = np.load(path + "/ssh.npy")
    nino34 = np.load(path + "/nino34.npy")
    print(path.split("/")[-1], "data_shape:", sst.shape, ssh.shape, nino34.shape)
    for i in range(ip_len):
        idr = -ip_len + i + 1 - op_len if -ip_len + i + 1 - op_len != 0 else None
        ip_data_sst = sst[i:idr][:, :, :, np.newaxis]
        ip_data_ssh = ssh[i:idr][:, :, :, np.newaxis]
        ip_data_ls.append(ip_data_sst)
        ip_data_ls1.append(ip_data_ssh)
    for j in range(op_len):
        idl = j + ip_len
        idr = -op_len + j + 1 if -op_len + j + 1 != 0 else None
        op_data = nino34[idl:idr][:, np.newaxis]
        op_data_ls.append(op_data)
    ip_data_ls = np.concatenate(ip_data_ls, axis=3)
    ip_data_ls1 = np.concatenate(ip_data_ls1, axis=3)
    op_data_ls = np.concatenate(op_data_ls, axis=1)
    if out_put_one is True:
        return ip_data_ls, ip_data_ls1, op_data_ls[:, -1]
    else:
        return ip_data_ls, ip_data_ls1, op_data_ls


def load_spmonth(path, ip_len=3, op_len=13, nino_month=1, label="noVar", out_put_one=True):
    # 　read data
    print(path)
    sst = np.load(path + "/sst.npy")
    ssh = np.load(path + "/ssh.npy")
    nino34 = np.load(path + "/nino34.npy")
    print(path.split("/")[-1], "Ini_data_shape:", sst.shape, ssh.shape, nino34.shape)
    if label == "noVar":
        bg_month = 2
    else:
        bg_month = 1
    ip_st_month = (nino_month - op_len - ip_len) % 12 + 1
    idx_begin = ip_st_month - bg_month
    nino_idx_begin = idx_begin + ip_len + op_len - 1
    N = sst.shape[0]
    gap_year = np.abs((nino_month - op_len - ip_len) // 12)
    op_data_ls = nino34[nino_idx_begin::12]
    ip_data_ls = []
    ip_data_ls1 = []
    for eh in range(ip_len):
        ip_data = sst[idx_begin + eh::12]
        ip_data1 = ssh[idx_begin + eh::12]
        diff_len = ip_data.shape[0] - op_data_ls.shape[0]
        if diff_len != 0:
            ip_data = ip_data[:-diff_len]
            ip_data1 = ip_data1[:-diff_len]
        ip_data_ls.append(ip_data[..., np.newaxis])
        ip_data_ls1.append(ip_data1[..., np.newaxis])
    ip_data_ls = np.concatenate(ip_data_ls, axis=-1)
    ip_data_ls1 = np.concatenate(ip_data_ls1, axis=-1)
    return ip_data_ls, ip_data_ls1, op_data_ls


def load_train(path, ip_len=3, op_len=20, with_obs=True, out_put_one=False, load0_func=load_var):
    fn_ls = os.listdir(path)
    ip_data_ls_ls = []
    ip_data_ls1_ls = []
    op_data_ls_ls = []
    for fn in fn_ls:
        if with_obs:
            ip_data_ls, ip_data_ls1, op_data_ls = load0_func(path + "/" + fn, ip_len, op_len, out_put_one=out_put_one)
            ip_data_ls_ls.append(ip_data_ls)
            ip_data_ls1_ls.append(ip_data_ls1)
            op_data_ls_ls.append(op_data_ls)
        else:
            if fn != "obs":
                ip_data_ls, ip_data_ls1, op_data_ls = load0_func(path + "/" + fn, ip_len, op_len,
                                                                 out_put_one=out_put_one)
                ip_data_ls_ls.append(ip_data_ls)
                ip_data_ls1_ls.append(ip_data_ls1)
                op_data_ls_ls.append(op_data_ls)

    ip_data_ls_ls = np.concatenate(ip_data_ls_ls, axis=0)
    ip_data_ls1_ls = np.concatenate(ip_data_ls1_ls, axis=0)
    op_data_ls_ls = np.concatenate(op_data_ls_ls, axis=0)
    print("=" * 80)
    print("All Data Shape:", ip_data_ls_ls.shape, ip_data_ls1_ls.shape, op_data_ls_ls.shape)
    print("=" * 80)
    return ip_data_ls_ls, ip_data_ls1_ls, op_data_ls_ls


if __name__ == "__main__":

    ip_data_ls, ip_data_ls1, op_data_ls = load_spmonth("../data/var_data", op_len=13, label="Var")
    print(ip_data_ls.shape, ip_data_ls1.shape, op_data_ls.shape)
